from django.contrib import admin
from django.core.exceptions import ValidationError
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
from import_export.formats import base_formats
from import_export.widgets import BooleanWidget, DecimalWidget, ForeignKeyWidget
import tablib

from .models import Category, Product, ProductVariant


VARIANT_SEPARATOR = "|"


class CategoryByNameWidget(ForeignKeyWidget):
    def clean(self, value, row=None, **kwargs):
        category_name = str(value or "").strip()
        if not category_name:
            raise ValidationError("Column 'category' is required for every imported product.")

        category, _ = Category.objects.get_or_create(name=category_name)
        return category

    def render(self, value, obj=None, **kwargs):
        return value.name if value else ""


class ProductResource(resources.ModelResource):
    category = fields.Field(
        column_name="category",
        attribute="category",
        widget=CategoryByNameWidget(Category, "name"),
    )
    price = fields.Field(
        column_name="price",
        attribute="price",
        widget=DecimalWidget(),
    )
    is_active = fields.Field(
        column_name="is_active",
        attribute="is_active",
        widget=BooleanWidget(),
    )
    variant_names = fields.Field(column_name="variant_names")
    variant_images = fields.Field(column_name="variant_images")

    class Meta:
        model = Product
        fields = (
            "id",
            "category",
            "name",
            "brand",
            "sku",
            "description",
            "price",
            "image",
            "is_active",
            "variant_names",
            "variant_images",
        )
        export_order = (
            "id",
            "category",
            "name",
            "brand",
            "sku",
            "description",
            "price",
            "image",
            "is_active",
            "variant_names",
            "variant_images",
        )
        skip_unchanged = True
        report_skipped = True
        clean_model_instances = True
        use_transactions = True

    @staticmethod
    def _split_variants(raw_value):
        if raw_value in (None, ""):
            return []

        normalized = str(raw_value).replace(";", VARIANT_SEPARATOR)
        parts = [part.strip() for part in normalized.split(VARIANT_SEPARATOR)]
        return [part for part in parts if part]

    def before_import_row(self, row, **kwargs):
        for key in (
            "category",
            "name",
            "brand",
            "sku",
            "description",
            "image",
            "variant_names",
            "variant_images",
        ):
            value = row.get(key)
            if isinstance(value, str):
                row[key] = value.strip()

        if not row.get("brand"):
            row["brand"] = Product._meta.get_field("brand").default

        if row.get("is_active") in (None, ""):
            row["is_active"] = "1"

        row_has_data = any(
            str(row.get(key, "")).strip()
            for key in ("id", "category", "name", "brand", "sku", "description", "price", "image", "variant_names", "variant_images")
        )
        if not row_has_data:
            return

        missing = [
            field_name
            for field_name in ("category", "name", "price")
            if not str(row.get(field_name, "")).strip()
        ]
        if missing:
            raise ValidationError(
                f"Missing required column values: {', '.join(missing)}."
            )

        variant_names = self._split_variants(row.get("variant_names"))
        variant_images = self._split_variants(row.get("variant_images"))
        if variant_images and len(variant_images) != len(variant_names):
            raise ValidationError(
                "variant_images must contain the same number of items as variant_names."
            )

    def get_instance(self, instance_loader, row):
        product_id = str(row.get("id") or "").strip()
        if product_id.isdigit():
            return Product.objects.filter(pk=product_id).first()

        sku = str(row.get("sku") or "").strip()
        if sku:
            return Product.objects.filter(sku=sku).first()

        name = str(row.get("name") or "").strip()
        category_name = str(row.get("category") or "").strip()
        if name and category_name:
            return Product.objects.filter(
                name=name,
                category__name=category_name,
            ).first()

        return None

    def after_save_instance(self, instance, row, **kwargs):
        if kwargs.get("dry_run"):
            return

        variant_names = self._split_variants(row.get("variant_names"))
        if not variant_names:
            return

        variant_images = self._split_variants(row.get("variant_images"))
        image_map = {}
        if variant_images:
            image_map = {
                variant_name: variant_images[index]
                for index, variant_name in enumerate(variant_names)
            }

        existing_variants = {
            variant.name: variant
            for variant in instance.variants.all()
        }

        kept_names = set()
        for variant_name in variant_names:
            variant, _ = ProductVariant.objects.get_or_create(
                product=instance,
                name=variant_name,
            )
            image_value = image_map.get(variant_name, "")
            if image_value:
                variant.image = image_value
                variant.save(update_fields=["image"])
            kept_names.add(variant_name)

        instance.variants.exclude(name__in=kept_names).delete()

    def dehydrate_variant_names(self, obj):
        return VARIANT_SEPARATOR.join(
            obj.variants.order_by("id").values_list("name", flat=True)
        )

    def dehydrate_variant_images(self, obj):
        image_names = []
        for variant in obj.variants.order_by("id"):
            image_names.append(variant.image.name if variant.image else "")
        return VARIANT_SEPARATOR.join(image_names)


class GoogleSheetsXLSX(base_formats.XLSX):
    def create_dataset(self, in_stream):
        from io import BytesIO

        import openpyxl

        xlsx_book = openpyxl.load_workbook(
            BytesIO(in_stream), read_only=False, data_only=True
        )

        dataset = tablib.Dataset()
        sheet = xlsx_book.active

        rows = list(sheet.iter_rows(values_only=True))
        if not rows:
            return dataset

        dataset.headers = list(rows[0])
        for row in rows[1:]:
            row_values = list(row)
            if all(value in (None, "") for value in row_values):
                continue
            dataset.append(row_values)
        return dataset


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    formats = [base_formats.CSV, GoogleSheetsXLSX]
    import_error_display = ("message", "row", "traceback")
    list_display = ("name", "brand", "sku", "price", "category", "is_active")
    list_editable = ("price", "is_active")
    list_filter = ("category", "brand", "is_active")
    search_fields = ("name", "brand", "sku", "description")
    autocomplete_fields = ("category",)
    filter_horizontal = ("compatible_products", "similar_products")
    inlines = [ProductVariantInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ("name",)

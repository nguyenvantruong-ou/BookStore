from flask_admin.contrib.sqla.filters import FilterLike, FilterNotLike, BooleanEqualFilter, BooleanNotEqualFilter, \
    FilterGreater, FilterEqual, FilterSmaller, FilterNotEqual
from flask_admin.form import rules
from wtforms import FileField, validators
from wtforms.validators import DataRequired
import cloudinary.uploader
from BookStoreApp import BookModel
from BookStoreApp.model_view.admin.base_model_view import BaseModelView


# Lớp này tượng trưng cho trang quản lý sách phía admin
class BookView(BaseModelView):
    # Thuộc tính hiển thị
    column_sortable_list = ['book_id',
                            'name',
                            'price',
                            'like_amount']
    column_searchable_list = ['name',
                              'price',
                              'like_amount']
    column_default_sort = 'book_id'
    column_labels = dict(book_id='Mã sách',
                         name='Tên sách',
                         price='Giá sách',
                         image='Ảnh bìa',
                         like_amount='Số lượt thích',
                         is_free_ship='Miễn phí vận chuyển',
                         sale='Phần trăm giảm giá',
                         point='Điểm',
                         manufacturer='Nhà xuất bản',
                         category='Loại sách',
                         description='Mô tả')

    # Lọc dữ liệu
    column_filters = (FilterLike(BookModel.name, name='Tên sách'),
                      FilterNotLike(BookModel.name, name='Tên sách'),
                      BooleanEqualFilter(BookModel.is_free_ship, name='Miễn phí vận chuyển'),
                      BooleanNotEqualFilter(BookModel.is_free_ship, name='Miễn phí vận chuyển'),
                      FilterEqual(BookModel.price, name='Giá'),
                      FilterNotEqual(BookModel.price, name='Giá'),
                      FilterGreater(BookModel.price, name='Giá'),
                      FilterSmaller(BookModel.price, name='Giá'),
                      FilterEqual(BookModel.like_amount, name='Số lượt thích'),
                      FilterNotEqual(BookModel.like_amount, name='Số lượt thích'),
                      FilterGreater(BookModel.like_amount, name='Số lượt thích'),
                      FilterSmaller(BookModel.like_amount, name='Số lượt thích'))

    # Form nhập thông tin
    form_rules = [
        rules.FieldSet(('name',
                        'price',
                        'image',
                        'is_free_ship',
                        'description'), 'Thông tin sách'),
        rules.FieldSet(('sale',
                        'point',
                        'manufacturer',
                        'category'), 'Thông tin khác có liên quan')
    ]
    form_extra_fields = {
        'image': FileField('Ảnh bìa')
    }
    form_args = dict(
        name=dict(validators=[DataRequired(), validators.Length(max=100)],
                  render_kw={
                      'placeholder': 'Tên sách...'
                  }),
        price=dict(validators=[DataRequired(), validators.NumberRange(min=1000, max=10000000)])
    )

    # Tải file khi tạo hoặc sửa thông tin sách
    def on_model_change(self, form, book_model, is_created):
        if form.image.data:
            res = cloudinary.uploader.upload(form.image.data, folder='book')
            book_model.set_image(str(res['secure_url']))
        else:
            book_model.set_image('https://res.cloudinary.com/attt92bookstore/image/upload/v1646019055/book'
                                 '/book_qmruxn.jpg')

    # Danh sách các cột hiển thị
    def scaffold_list_columns(self):
        return ['book_id',
                'name',
                'price',
                'like_amount',
                'is_free_ship',
                'image',
                'description',
                'sale',
                'point',
                'category',
                'manufacturer']

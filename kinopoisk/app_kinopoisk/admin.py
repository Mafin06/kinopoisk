from django import forms
from django.contrib import admin
from .models import Category, Movie, MovieShots, Actor, RatingStar, Rating, Reviews, Genre
# Register your models here.
from django.utils.safestring import mark_safe # для вывода изображений


from ckeditor_uploader.widgets import CKEditorUploadingWidget 
class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(label="Описание", widget=CKEditorUploadingWidget ())
    class Meta:
        model = Movie
        fields = '__all__'





@admin.register(Category) #можно регистрировать модели в админке с помощью декоратора
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url" )
    list_display_links = ("name", )

#admin.site.register(Category, CategoryAdmin)
    #еще один класс для отзывов чтобы видеть только их при просмотре фильмов в админке
class ReviewsInLine(admin.TabularInline):#TabularInline - это класс, который используется для отображения связанных объектов в табличном формате на странице редактирования родительской модели (почти то же самое что и StackedInline)
    model = Reviews
    extra = 1 # 1 пустой отзыв который мы сможем добавить из админки
    readonly_fields = ("email", "name")
@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "movie", "get_image")
    list_display_links = ("title", )
    readonly_fields = ("get_image", )
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60">')#метод для пометки строки как безопасной для вывода в формате HTML
    get_image.short_description = "Изображение"

class MovieShotsInline(admin.TabularInline):#StackedInline - класс, который используется для отображения и редактирования связанных моделей в интерфейсе администратора для родительской модели.
    model = MovieShots
    extra = 1
    readonly_fields = ("get_image", )
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="100">')#метод для пометки строки как безопасной для вывода в формате HTML
    get_image.short_description = "Изображение"

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    form = MovieAdminForm
    # list_display = ("title", "category", "url", "draft")
    list_filter = ("category", "year")
    search_fields = ("title", "category__name", )
    inlines = [MovieShotsInline, ReviewsInLine]#StackedInline
    save_on_top = True #меню удаления и сохранения наверху закрепить 
    save_as = True #сохранить как новый обьект - дублированный 
    # list_editable = ("draft", )#чтобы редактировать поле прямо сразу не заходя в фильм
    #fields = (("actors", "directors","genres"), )#в одну строку
    actions = ["publish", "unpublish"]
    # readonly_fields =("get_image", )
    # fieldsets = (
    #     (None, {
    #         "fields":(("title", "tagline"),)
    #     }),
    #     (None, {
    #         "fields":("description", ("poster", "get_image"),)
    #     }),
    #     (None, {
    #         "fields":(("year", "country", "world_premiere"),)
    #     }),
    #     ("Actors", {#название группы
    #         "classes": ("collapse", ),# свернутый вид
    #         "fields":(("directors", "actors", "genres", "category"),)
    #     }),
    #     (None, {
    #         "fields":(("fees_in_usa", "fees_in_world", "budget"),)
    #     }),
    #     ("Options", {
    #         "fields":(("draft", "url"),)
    #     }),
        
    # )
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="400" height="auto">')#метод для пометки строки как безопасной для вывода в формате HTML
    get_image.short_description = "Постер"

    def unpublish(self, request, queryset):
        """снять с публикации"""
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = "1 запись обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f'{message_bit}')

    def publish(self, request, queryset):
        """публикация"""
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = "1 запись обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f'{message_bit}')

    unpublish.short_description = "Снять с публикации"
    unpublish.allowed_permissions = ('change',)
    publish.short_description = "Опубликовать"
    publish.allowed_permissions = ('change',)
        

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "get_image")
    list_display_links = ("name", )
    readonly_fields = ("get_image", )
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60">')#метод для пометки строки как безопасной для вывода в формате HTML
    get_image.short_description = "Изображение"#в админке при редактировании записи эта картинка подписана как "изображение"

@admin.register(RatingStar)
class RatingStarAdmin(admin.ModelAdmin):
    list_display = ("id", "value",  )
    list_display_links = ("value", )

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("id", "star", "movie", "ip", "get_user_ip" )
    list_display_links = ("star", )
    search_fields = ('ip', 'movie__title')
    def get_user_ip(self, obj):
        return obj.ip
    get_user_ip.short_description = 'IP адрес (через метод)'

@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "parent", "movie", "id")
    readonly_fields = ("name", "email")

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url", "description" )
    list_display_links = ("name", )

admin.site.site_title = "Django Kinopoisk"
admin.site.site_header = "Django Kinopoisk"
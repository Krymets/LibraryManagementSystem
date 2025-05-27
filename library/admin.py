from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Book, Loan

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_admin', 'is_active')
    list_filter = ('is_admin', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'page_count', 'available')
    list_filter = ('available', 'author')
    search_fields = ('title', 'author', 'isbn')
    ordering = ('title',)

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'borrowed_at', 'returned_at', 'is_returned')
    list_filter = ('returned_at',)
    search_fields = ('user__username', 'book__title')
    ordering = ('-borrowed_at',)
    readonly_fields = ('borrowed_at',)

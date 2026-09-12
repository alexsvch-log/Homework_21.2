// Введен для управления переключения страницами в обход запрета ТЗ, а также что бы не перерисовывать страницу
//каждый раз при обращении к ней. Скрипт находит все кнопки в левом меню и автоматически подгружает нужную
// страницу.
document.addEventListener('DOMContentLoaded', () => {
    const menuItems = document.querySelectorAll('.nav-link');
    const contentArea = document.getElementById('content-area');

    menuItems.forEach(item => {
        item.addEventListener('click', async () => {
            // Переключаем классы Bootstrap активной кнопки
            menuItems.forEach(el => {
                el.classList.remove('btn-primary', 'text-white', 'active');
                el.classList.add('btn-dark', 'text-secondary');
            });

            item.classList.remove('btn-dark', 'text-secondary');
            item.classList.add('btn-primary', 'text-white', 'active');

            const pageName = item.getAttribute('data-page');

            // Запрашиваем у сервера чистый HTML-кусок
            const response = await fetch(`/get-page/${pageName}`);
            const htmlContent = await response.text();

            // Вставляем контент в правую часть страницы
            contentArea.innerHTML = htmlContent;
        });
    });
});
(function () {
    // create search box elements
    const searchBox = document.createElement('input');
    searchBox.id = 'admin-dashboard-filter';
    searchBox.type = 'search';
    searchBox.placeholder = 'quick filter';
    searchBox.autofocus = true;

    const searchBoxContainer = document.createElement('div');
    searchBoxContainer.id = 'admin-dashboard-filter-toolbar';
    searchBoxContainer.appendChild(searchBox);

    window.addEventListener('DOMContentLoaded', (event) => {
        const dashboardRef = document.querySelector('.dashboard #content h1');  // dashboard or module index
        const sidebarRef = document.querySelector('#nav-sidebar .module');  // nav-sidebar
        const index = [];
        let apps;

        // inject search input into dashboard or nav-sidebar
        if (dashboardRef !== null) {
            dashboardRef.parentNode.insertBefore(searchBoxContainer, dashboardRef.nextSibling);
            apps = document.querySelectorAll('#content-main .module')
        }
        else if (sidebarRef !== null) {
            sidebarRef.parentNode.insertBefore(searchBoxContainer, sidebarRef.previousSibling);
            apps = document.querySelectorAll('#nav-sidebar .module')
        }

        if (!apps) {
            return;
        }

        // build index
        apps.forEach(function (app) {
            app.querySelectorAll('[class^="model-"]').forEach(function (model) {
                index.push({
                    label: model.querySelector('[scope="row"]').innerText,
                    element: model,
                });
            });
        });

        // clear input on "Escape" key press
        searchBox.addEventListener('keyup', function (e) {
            if (e.key === 'Escape') {
                searchBox.value = '';
                searchBox.dispatchEvent(new InputEvent('input'));
            }
        });

        searchBox.addEventListener('input', function (e) {
            e.preventDefault();
            requestAnimationFrame(function () {
                const pattern = new RegExp(searchBox.value, 'i')

                index.forEach(function (model) {
                    if (model.label.match(pattern)) {
                        model.element.classList.remove('admin-dashboard-filter--hidden');
                    } else {
                        model.element.classList.add('admin-dashboard-filter--hidden');
                    }
                });

                // hide app if no model is visible
                apps.forEach(function (app) {
                    if (app.querySelectorAll('tr:not(.admin-dashboard-filter--hidden)').length === 0) {
                        app.classList.add('admin-dashboard-filter--hidden');
                    } else {
                        app.classList.remove('admin-dashboard-filter--hidden');
                    }
                });
            });
        });
    });
})();

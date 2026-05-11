document.addEventListener('DOMContentLoaded', () => {

    const confirmationForms = document.querySelectorAll(
        '[data-confirm]'
    );

    confirmationForms.forEach(form => {

        form.addEventListener('submit', (event) => {

            const message = form.dataset.confirm;

            const confirmed = confirm(message);

            if (!confirmed) {
                event.preventDefault();
            }

        });

    });

});
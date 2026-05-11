setTimeout(() => {

    const alerts = document.querySelectorAll('.alert');

    alerts.forEach(alert => {

        alert.style.opacity = '0';
        alert.style.transform = 'translateY(-10px)';

        setTimeout(() => {
            alert.remove();
        }, 400);

    });

}, 4000);
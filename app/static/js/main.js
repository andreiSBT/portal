// Custom JavaScript for To-Do List Application

document.addEventListener('DOMContentLoaded', function() {
    // Delete confirmation for tasks and categories
    const deleteForms = document.querySelectorAll('.delete-form');

    deleteForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const confirmed = confirm('Are you sure you want to delete this item? This action cannot be undone.');

            if (!confirmed) {
                e.preventDefault();
            }
        });
    });

    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Add active class to current filter button
    const filterButtons = document.querySelectorAll('.btn-group .btn');
    filterButtons.forEach(button => {
        if (button.classList.contains('active')) {
            button.style.fontWeight = '600';
        }
    });

    // Color picker synchronization (for category forms)
    const colorInputs = document.querySelectorAll('input[type="color"]');
    colorInputs.forEach(colorInput => {
        const textInput = colorInput.nextElementSibling;

        if (textInput && textInput.type === 'text') {
            // Sync color picker to text input
            colorInput.addEventListener('input', function() {
                textInput.value = this.value;
            });

            // Sync text input to color picker
            textInput.addEventListener('input', function() {
                if (/^#[0-9A-Fa-f]{6}$/.test(this.value)) {
                    colorInput.value = this.value;
                }
            });
        }
    });

    // Form validation feedback
    const forms = document.querySelectorAll('form[novalidate]');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Highlight overdue tasks
    const overdueTasks = document.querySelectorAll('.text-danger.fw-bold');
    overdueTasks.forEach(task => {
        task.parentElement.parentElement.style.borderColor = '#dc3545';
    });

    // Add tooltips to buttons (Bootstrap tooltips)
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Smooth scroll to top button (optional enhancement)
    const scrollButton = document.createElement('button');
    scrollButton.innerHTML = '<i class="bi bi-arrow-up-circle-fill"></i>';
    scrollButton.className = 'btn btn-primary rounded-circle position-fixed bottom-0 end-0 m-4';
    scrollButton.style.display = 'none';
    scrollButton.style.zIndex = '1000';
    scrollButton.style.width = '50px';
    scrollButton.style.height = '50px';

    document.body.appendChild(scrollButton);

    window.addEventListener('scroll', function() {
        if (window.scrollY > 300) {
            scrollButton.style.display = 'block';
        } else {
            scrollButton.style.display = 'none';
        }
    });

    scrollButton.addEventListener('click', function() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // Task card animation on load
    const taskCards = document.querySelectorAll('.task-card');
    taskCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';

        setTimeout(() => {
            card.style.transition = 'opacity 0.5s, transform 0.5s';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 50);
    });

    console.log('To-Do List App initialized successfully!');
});

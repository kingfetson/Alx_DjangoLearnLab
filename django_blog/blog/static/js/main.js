// Main JavaScript for Django Blog

document.addEventListener('DOMContentLoaded', function() {
    console.log('Django Blog loaded successfully!');
    
    // Add smooth scrolling to all links
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Form validation for post creation/editing
    const postForm = document.querySelector('.post-form');
    if (postForm) {
        postForm.addEventListener('submit', function(e) {
            const title = document.getElementById('id_title');
            const content = document.getElementById('id_content');
            
            if (title.value.trim() === '') {
                e.preventDefault();
                alert('Please enter a title for your post.');
                title.focus();
                return false;
            }
            
            if (content.value.trim() === '') {
                e.preventDefault();
                alert('Please enter some content for your post.');
                content.focus();
                return false;
            }
        });
    }
    
    // Add confirmation for delete actions
    const deleteButtons = document.querySelectorAll('.delete-post');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this post? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });
    
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s';
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.style.display = 'none';
            }, 500);
        }, 5000);
    });
});
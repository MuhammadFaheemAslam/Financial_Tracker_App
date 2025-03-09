document.addEventListener("DOMContentLoaded", function () {
    // Show all toast messages
    let toastElList = [].slice.call(document.querySelectorAll('.toast'));
    toastElList.forEach(function (toastEl) {
        let toast = new bootstrap.Toast(toastEl);
        toast.show();
    });
});

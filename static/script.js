function togglePasswordVisibility() {
    var passwordInput = document.getElementsByName("password")[0];
    var eyeIcons = document.querySelectorAll(".bi-eye");

    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        eyeIcons.forEach(function(eyeIcon) {
            eyeIcon.classList.remove("bi-eye");
            eyeIcon.classList.add("bi-eye-slash");
        });
    } else {
        passwordInput.type = "password";
        eyeIcons.forEach(function(eyeIcon) {
            eyeIcon.classList.remove("bi-eye-slash");
            eyeIcon.classList.add("bi-eye");
        });
    }
}

document.addEventListener("DOMContentLoaded", function() {
    var eyeIcons = document.querySelectorAll(".bi-eye");
    eyeIcons.forEach(function(eyeIcon) {
        eyeIcon.addEventListener("click", togglePasswordVisibility);
    });

    var userTypeSelect = document.querySelector('select[name="usertype"]');

    var farmLocationLabel = document.getElementById('farm_location_label');
    var farmLocationInput = document.getElementById('farm_location_input');

    var farmSizeLabel = document.getElementById('farm_size_label');
    var farmSizeInput = document.getElementById('farm_size_input');

    var companyNameLabel = document.getElementById('company_name_label');
    var companyNameInput = document.getElementById('company_name_input');

    function handleUserTypeChange() {
        var userType = userTypeSelect.value;

        farmLocationInput.style.display = "none";
        farmLocationLabel.style.display = "none";
        farmSizeInput.style.display = "none";
        farmSizeLabel.style.display = "none";
        companyNameInput.style.display = "none";
        companyNameLabel.style.display = "none";

        if (userType === "customer") {
            farmLocationInput.style.display = "block";
            farmLocationLabel.style.display = "block";
            farmSizeInput.style.display = "block";
            farmSizeLabel.style.display = "block";
        } else if (userType === "stakeholder") {
            companyNameInput.style.display = "block";
            companyNameLabel.style.display = "block";
        }
    }

    // Add event listener for user type change
    userTypeSelect.addEventListener('change', handleUserTypeChange);

    // Call the function initially to set the default state
    handleUserTypeChange();
});


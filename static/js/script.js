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

    // investor
    var fullnameLabel = document.getElementById('fullnameLabel');
    var fullnameInput = document.getElementById('fullname');
    var aadharLabel = document.getElementById('aadharLabel');
    var aadharInput = document.getElementById('aadhar');
    var usernameLabel = document.getElementById('usernameLabel');
    var usernameInput = document.getElementById('username');
    var passwordLabel = document.getElementById('passwordLabel');
    var passwordInput = document.getElementById('password');
    var passwordInputSvg = document.getElementById('passwordsvg');

    // farmer
    var farmLocationLabel = document.getElementById('farm_location_label');
    var farmLocationInput = document.getElementById('farm_location_input');
    var farmSizeLabel = document.getElementById('farm_size_label');
    var farmSizeInput = document.getElementById('farm_size_input');

    // company
    var companyNameLabel = document.getElementById('company_name_label');
    var companyNameInput = document.getElementById('company_name_input');
    var companyPasswordLabel = document.getElementById('company_password_label');
    var companyPasswordInput = document.getElementById('company_password_input');
    var companyPasswordInputSvg = document.getElementById('company_password_input_svg');
    
    var companyTypeSelect = document.querySelector('select[name = "companytype"]')
    var companyTypeLabel = document.getElementById('company_type_label');
    var companyTypeInput = document.getElementById('company_type_input');


    function handleUserTypeChange() {
        var userType = userTypeSelect.value;

        farmLocationInput.style.display = "none";
        farmLocationLabel.style.display = "none";
        farmSizeInput.style.display = "none";
        farmSizeLabel.style.display = "none";
        companyNameInput.style.display = "none";
        companyNameLabel.style.display = "none";
        companyPasswordInput.style.display = "none";
        companyPasswordLabel.style.display = "none";
        companyTypeInput.style.display = "none";
        companyTypeLabel.style.display = "none";
        companyPasswordInputSvg.style.display = "none";

        if (userType === "investor") {
            
            fullnameInput.style.display = "block";
            fullnameLabel.style.display = "block";
            aadharInput.style.display = "block";
            aadharLabel.style.display = "block";
            usernameInput.style.display = "block";
            usernameLabel.style.display = "block";
            passwordInput.style.display = "block";   
            passwordLabel.style.display = "block";
            passwordInputSvg.style.display = "block";
        }
        
        else if (userType === "farmer") {
            farmLocationInput.style.display = "block";
            farmLocationLabel.style.display = "block";
            farmSizeInput.style.display = "block";
            farmSizeLabel.style.display = "block";
        } 
        else if (userType === "company") {

            fullnameInput.style.display = "none";
            fullnameLabel.style.display = "none";
            aadharInput.style.display = "none";
            aadharLabel.style.display = "none";
            usernameInput.style.display = "none";
            usernameLabel.style.display = "none";
            passwordInput.style.display = "none";   
            passwordLabel.style.display = "none";
            passwordInputSvg.style.display = "none";

            companyNameInput.style.display = "block";
            companyNameLabel.style.display = "block";
            companyPasswordInput.style.display = "block";
            companyPasswordLabel.style.display = "block";
            companyTypeInput.style.display = "block";
            companyTypeLabel.style.display = "block";
            companyPasswordInputSvg.style.display = "block";
        }
    }

    // Add event listener for user type change
    userTypeSelect.addEventListener('change', handleUserTypeChange);

    // Call the function initially to set the default state
    handleUserTypeChange();

    // Function to handle company type change and show/hide subcategories
    function handleCompanyTypeChange() {
        const companyTypeSelect = document.getElementById('company_type_input');
        const selectedType = companyTypeSelect.value;

        // Hide all sections
        document.getElementById('seeds-subcategories').classList.add('hidden');
        document.getElementById('equipment-subcategories').classList.add('hidden');

        // Show the selected section
        if (selectedType === 'seeds') {
            document.getElementById('seeds-subcategories').classList.remove('hidden');
        } else if (selectedType === 'equipment') {
            document.getElementById('equipment-subcategories').classList.remove('hidden');
        }
    }

    // Event listener for company type selection
    companyTypeSelect.addEventListener('change', handleCompanyTypeChange);
});



    const checkall = document.getElementById("checkAll");
    const checks = document.query.querySelectorAll(".checks");

    checkall.addEventListener('click', () => {
        for (val of checks) {
            checkall.checked == true ? val.checked = true : val.checked = false;
        }
    });
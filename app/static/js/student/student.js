    document.getElementById("courseSelect").addEventListener("change", function () {
        let courseId = this.value;
        let semesterSelect = document.getElementById("semesterSelect");

        // clear old options
        semesterSelect.innerHTML = '<option value="">All Semesters</option>';

        if (courseId) {
            fetch(`/api/courses/${courseId}/semesters`)
                .then(response => response.json())
                .then(data => {
                    data.semesters.forEach(sem => {
                        let opt = document.createElement("option");
                        opt.value = sem.id;
                        opt.textContent = "Semester " + sem.number;
                        semesterSelect.appendChild(opt);
                    });
                });
        }
    });

    function confirmDelete(form) {
    return confirm("Are you sure you want to delete this student?");
}

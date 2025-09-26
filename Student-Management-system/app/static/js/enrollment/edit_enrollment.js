    document.getElementById("student-search").addEventListener("input", async function () {

        let query = this.value;
        if (query.length < 2) return;

        let res = await fetch(`/students/search?query=${query}`);
        let students = await res.json();

        let resultsDiv = document.getElementById("search-results");
        resultsDiv.innerHTML = "";
        students.forEach(st => {
            let div = document.createElement("div");
            div.innerText = st.name + " (" + st.id + ")";
            div.onclick = function () {
                document.getElementById("student-search").value = st.name;
                document.getElementById("student-id").value = st.id;
                resultsDiv.innerHTML = "";
            }
            resultsDiv.appendChild(div);
        });
    });
   let currentSemesterId = "{{ enroll.semester.id }}";  // from backend

document.getElementById("courseSelect").addEventListener("change", function () {
    let courseId = this.value;
    let semesterSelect = document.getElementById("semesterSelect");

    semesterSelect.innerHTML = '<option value="">-- Select Semester --</option>';

    if (courseId) {
        fetch(`/api/courses/${courseId}/semesters`)
            .then(response => response.json())
            .then(data => {
                data.semesters.forEach(sem => {
                    let opt = document.createElement("option");
                    opt.value = sem.id;
                    opt.textContent = "Semester " + sem.number;
                    if (sem.id == currentSemesterId) {
                        opt.selected = true; // ✅ auto-select saved semester
                    }
                    semesterSelect.appendChild(opt);
                });
            });
    }
});

// 👇 Trigger change on page load to auto-fill semesters
document.getElementById("courseSelect").dispatchEvent(new Event("change"));
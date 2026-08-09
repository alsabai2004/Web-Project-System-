// ===== 1. تسجيل الدخول =====
function login() {
    let username = document.getElementById("username").value;
    let password = document.getElementById("pass").value;

    if (username === "admin" && password === "1234") {
        localStorage.setItem("loggedIn", "true");
        alert("تم تسجيل الدخول بنجاح");
        location.href = "home.html";
    } else {
        alert("خطأ في تسجيل الدخول");
    }
}

// ===== 2. التحقق من تسجيل الدخول في كل الصفحات =====
if (window.location.pathname.includes("home.html") || 
    window.location.pathname.includes("add.html") || 
    window.location.pathname.includes("view.html") || 
    window.location.pathname.includes("delete.html") ||
    window.location.pathname.includes("end.html")) {
    
    let loggedIn = localStorage.getItem("loggedIn");
    if (loggedIn !== "true") {
        location.href = "index.html";
    }
}

// ===== 3. دوال التخزين =====
function getStudents() {
    let students = localStorage.getItem("students");
    if (students === null) {
        return [];
    } else {
        return JSON.parse(students);
    }
}

function saveStudents(students) {
    localStorage.setItem("students", JSON.stringify(students));
}

// ===== 4. تحديث عدد الطلاب في الصفحة الرئيسية =====
function updateTotalCount() {
    let totalSpan = document.getElementById("totalCount");
    if (totalSpan) {
        let students = getStudents();
        totalSpan.innerHTML = students.length;
    }
}

// ===== 5. إضافة طالب =====
function addStudent() {
    let student_id = document.getElementById("id").value;
    let student_name = document.getElementById("name").value;
    let student_department = document.getElementById("department").value;
    let student_level = document.getElementById("level").value;
    let student_gpa = document.getElementById("gpa").value;

    if (student_id === "" || student_name === "") {
        alert("الرجاء ملء جميع الحقول");
        return;
    }

    let students = getStudents();
    
    // منع تكرار ID
    let idExists = false;
    for (let i = 0; i < students.length; i++) {
        if (students[i].id === student_id) {
            idExists = true;
            break;
        }
    }
    
    if (idExists === true) {
        alert("❌ هذا الرقم موجود مسبقاً");
        return;
    }

    let student = {
        id: student_id,
        name: student_name,
        department: student_department,
        level: student_level,
        gpa: student_gpa
    };

    students.push(student);
    saveStudents(students);

    let resultDiv = document.getElementById("addResult");
    resultDiv.style.display = "block";
    resultDiv.innerHTML = `
        <h3 style="color:#10b981;">✅ تمت إضافة الطالب</h3>
        <p><strong>ID:</strong> ${student_id}</p>
        <p><strong>الاسم:</strong> ${student_name}</p>
        <p><strong>القسم:</strong> ${student_department}</p>
        <p><strong>المستوى:</strong> ${student_level}</p>
        <p><strong>المعدل:</strong> ${student_gpa}</p>
    `;

    // تفريغ الحقول
    document.getElementById("id").value = "";
    document.getElementById("name").value = "";
    document.getElementById("department").value = "";
    document.getElementById("level").value = "";
    document.getElementById("gpa").value = "";

    updateTotalCount();
}

// ===== 6. عرض جميع الطلاب =====
function displayStudents() {
    let students = getStudents();
    let container = document.getElementById("studentsList");

    if (students.length === 0) {
        container.innerHTML = '<div class="empty-message">📭 لا يوجد طلاب حالياً</div>';
        return;
    }

    let table = '<table border="0" cellspacing="0" cellpadding="10">';
    table = table + '<tr><th>ID</th><th>الاسم</th><th>القسم</th><th>المستوى</th><th>المعدل</th></tr>';

    for (let i = 0; i < students.length; i++) {
        let student = students[i];
        table = table + `
            <tr>
                <td>${student.id}</td>
                <td>${student.name}</td>
                <td>${student.department}</td>
                <td>${student.level}</td>
                <td>${student.gpa}</td>
            </tr>
        `;
    }

    table = table + '</table>';
    container.innerHTML = table;
}

// ===== 7. حذف طالب =====
function deleteStudent() {
    let deleteId = document.getElementById("deleteId").value;
    let resultDiv = document.getElementById("deleteResult");

    if (deleteId === "") {
        alert("الرجاء إدخال رقم الطالب");
        return;
    }

    let students = getStudents();
    let found = false;
    let newStudents = [];

    for (let i = 0; i < students.length; i++) {
        if (students[i].id !== deleteId) {
            newStudents.push(students[i]);
        } else {
            found = true;
        }
    }

    if (found === true) {
        saveStudents(newStudents);
        resultDiv.style.display = "block";
        resultDiv.className = "result success";
        resultDiv.innerHTML = "<p>✅ تم حذف الطالب بنجاح</p>";
        document.getElementById("deleteId").value = "";
        updateTotalCount();
    } else {
        resultDiv.style.display = "block";
        resultDiv.className = "result error";
        resultDiv.innerHTML = "<p>❌ لا يوجد طالب بهذا الرقم</p>";
    }
}

// ===== 8. تسجيل الخروج =====
function logout() {
    localStorage.removeItem("loggedIn");
}

var dept1 = document.getElementsByName('dept1');
var dept2 = document.getElementsByName('dept2');
var dept3 = document.getElementsByName('dept3');

var change = function(dept, id) {
    var courseList = document.getElementById(id);
    $.post('/departments',
	   {
	       department: dept
	   },
	   function(courses) {
	       courses = JSON.parse(courses);
    	       courseList.options.length = 0;
	       courseList.options[0] = new Option('', '');
	       for (var i = 0; i < courses.length; i++) {
		   courseList.options[courseList.options.length] = new Option(courses[i], courses[i]);
	       }
	   });
}

function addListener(element, value, course) {
    element.addEventListener('click', function() {
	change(value, course)
    });
}

for (var i = 0; i < dept1.length; i++) {
    addListener(dept1[i], dept1[i].value, 'course1');
}

for (i = 0; i < dept2.length; i++) {
    addListener(dept2[i], dept2[i].value, 'course2');
}

for (i = 0; i < dept3.length; i++) {
    addListener(dept3[i], dept3[i].value, 'course3');
}

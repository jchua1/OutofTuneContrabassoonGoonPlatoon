//list of course pref 1 radio buttons
var dept1 = document.getElementsByName('dept1');
//list of course pref 2 radio buttons
var dept2 = document.getElementsByName('dept2');
//list of course pref 3 radio buttons
var dept3 = document.getElementsByName('dept3');

//function that uses a post ajax call to populate the drop down menu with courses from the department of the checked radio button
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

//adds change() as a function that triggers on click to the given element
function addListener(element, value, course) {
    element.addEventListener('click', function() {
	change(value, course)
    });
}

//loops through list of course pref 1 radio buttons and adds change() as a function that triggers on click to each button
for (var i = 0; i < dept1.length; i++) {
    addListener(dept1[i], dept1[i].value, 'course1');
}

//loops through list of course pref 2 radio buttons and adds change() as a function that triggers on click to each button
for (i = 0; i < dept2.length; i++) {
    addListener(dept2[i], dept2[i].value, 'course2');
}

//loops through list of course pref 3 radio buttons and adds change() as a function that triggers on click to each button
for (i = 0; i < dept3.length; i++) {
    addListener(dept3[i], dept3[i].value, 'course3');
}

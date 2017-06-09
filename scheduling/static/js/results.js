var keys = [];
var reqs = [];

//get ajax call to populate keys and reqs with data for the d3 bar graph
$.get('/responses',
      function(courseNum) {
	  courseNum = JSON.parse(courseNum);
	  var temp = Object.keys(courseNum);
	  for (var i = 0; i < temp.length; i++) {
	      keys.push(temp[i]);
	      reqs.push(courseNum[temp[i]]);
	  }
      });

//creates d3 bar graph (does not work)
 d3.select(".chart")
    .selectAll("div")
    .data(reqs)
    .enter()
    .append("div")
    .style("width", function(d) {
        return d*15 + "px";
    })
    .data(keys)
    .text(function(d) {
        return d;
    })

//list of department radio buttons
var dept = document.getElementsByName('dept');

//function that uses a post ajax call to populate the drop down menu with courses from the department of the checked radio button
var change = function(dept) {
    var courseList = document.getElementById('course');
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
function addListener(element, value) {
    element.addEventListener('click', function() {
	change(value)
    });
}

//loops through list of department radio buttons and adds change() as a function that triggers on click to each button
//adds a second on-click function that finds the checked radio button and uses an ajax call to edit deptData in __init__.py, populating it with responses from all teachers who requested a course in the department of the checked radio button
for (var i = 0; i < dept.length; i++) {
    addListener(dept[i], dept[i].value);
    dept[i].addEventListener('click', function() {
    for (var i = 0; i < dept.length; i++) {
	if (dept[i].checked) {
	    var d = dept[i].value;
	    console.log(d);
	    break;
	}
    }
    $.post('/deptResponses',
	   {
	       dept: d
	   },
	   function(ret) {
	       console.log('hi');
	   });
    });
}

//drop down menu
var course = document.getElementById('course');
//unordered list
var list = document.getElementById('list');

//adds an on-change function to the drop down menu that uses a post ajax call to populate the unordered list with responses from teachers who requested the selected course in the drop down menu
course.addEventListener('change', function() {
    list.innerHTML = '';
    $.post('/teachers',
	   {
	       course: course.value
	   },
	   function(teachers) {
	       teachers = JSON.parse(teachers);
	       for (var i = 0; i < teachers.length; i++) {
		   var entry = document.createElement('li');
		   entry.appendChild(document.createTextNode(teachers[i]));
		   list.appendChild(entry);
	       }
	   });
});

//initial population of deptData in __init__.py with responses from teacher who requested a couse in the Art department
$.post('/deptResponses',
       {
	   dept: 'Art'
       },
       function(ret) {
	   return ret
       });

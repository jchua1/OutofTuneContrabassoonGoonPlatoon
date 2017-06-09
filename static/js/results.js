var graph = d3.select();

var keys = [];
var reqs = [];

$.get('/responses',
      function(courseNum) {
	  courseNum = JSON.parse(courseNum);
	  var temp = Object.keys(courseNum);
	  for (var i = 0; i < temp.length; i++) {
	      keys.push(temp[i]);
	      reqs.push(courseNum[temp[i]]);
	  }
      });

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

var dept = document.getElementsByName('dept');

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

function addListener(element, value) {
    element.addEventListener('click', function() {
	change(value)
    });
}

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

var course = document.getElementById('course');
var list = document.getElementById('list');

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

$.post('/deptResponses',
       {
	   dept: 'Art'
       },
       function(ret) {
	   return ret
       });

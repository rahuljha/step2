

Task_ui_handler = function() {
    this.task_table = null;
    var _this = this;
    
    this.load_task_table = function(tasks) {
        taskArray = new Array();
        for(task in tasks) {
            taskData = tasks[task];
            taskArray.push(new Array("<a href='/projects/tasks/"+taskData['id']+"'>"+taskData['title']+"</a>", 
                                     taskData['created_date'], 
                                     taskData['due_date'],
                                     taskData['assigned_to']['username'],
                                     taskData['state'])
                          );
        }
        
        _this.task_table = $('#task_list').dataTable({
		                                         "aaData": taskArray,
		                                         "aoColumns": [
		                                             { "sTitle": "Task" },
		                                             { "sTitle": "Start Date", "sClass": "center"},
		                                             { "sTitle": "End Date", "sClass": "center" },
	                                                     { "sTitle": "Assigned To", "sClass": "center"},
		                                             { "sTitle": "State"}
		                                         ],
                                                         "iDisplayLength": 5,
                                                         "sPaginationType": "full_numbers"
	                                             });	
        
    };

    this.update_task_table = function(title, created_date, due_date, assigned_to, state) {
        _this.task_table.fnAddData([title, created_date, due_date, assigned_to, state]);
    };

};

var task_ui_handler = new Task_ui_handler();


init_dialogs = function() {

    $('#dialog_add_task').dialog({
                                     autoOpen: false,
			             height: 500,
			             width: 300,
			             modal: true,
                                     buttons: {
                                         'Add Task': function() {

                                             post_data = {
                                                 title: $('#new_task_title').val(),
                                                 description: $('#new_task_desc').val(),
                                                 belongs_to_project: $('#belongs_to_project').val(),
                                                 due_date: $('#new_task_due_date').val(),
                                                 created_date: $('#new_task_created_date').val(),
                                                 state: $('#new_task_state').val(),
                                                 assigned_to: $('#new_task_assigned_to option:selected').attr('id')
                                             };
                                             
                                             $.ajax({
                                                        url: '/api/projects/tasks/',
                                                        type: 'POST',
                                                        contentType: 'application/json',
                                                        data: JSON.stringify(post_data),
                                                        username: 'rahuljha',
                                                        password: 'Rahul222486',
                                                        success: function(retval) {
                                                            task_ui_handler.update_task_table($('#new_task_title').val(), 
                                                                                              $('#new_task_created_date').val(), 
                                                                                              $('#new_task_due_date').val(),
                                                                                              $('#new_task_assigned_to option:selected').text(),
                                                                                              $('#new_task_state').val()
                                                                                             );

					                    $('#dialog_add_task').dialog('close');
                                                        },
                                                        error: function(obj, text, error) {
                                                            alert(text);
					                    $('#dialog_add_task').dialog('close');
                                                        }
                                                    });
                                             
                                         },
                                         Cancel: function() {
                                            
					     $(this).dialog('close');
				         }
                                     },
                                     close: function() {
			             }

                                 });
    $('.date_picker').datepicker({ dateFormat: 'yy-mm-dd' });
};

init_buttons = function() {
    $('#add_task').click(function() {
                             $('#dialog_add_task').dialog('open');
                             return false;
                         });
};

$(document).ready(

    function() {
        $.ajax({
                   url: "/api/projects/1/tasks",
	           type: 'GET',
                   dataType: 'json',
                   timeout: 5000,
                   success: task_ui_handler.load_task_table
               });

        init_dialogs();
        init_buttons();
        $('#project_description p').jTruncate({
                                                  moreText: "expand",
                                                  lessText: "collapse",
                                                  moreAni: "fast",
                                                  lessAni: "fast"
                                              });
    }
);
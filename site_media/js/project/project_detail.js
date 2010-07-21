Util = function() {
    this.create_task_link = function(task_id,task_title) {
        return "<a href='/projects/tasks/"+task_id+"'>"+task_title+"</a>";
    };
    
    this.create_ops_links = function(task_id, task_title) {
        edit_link = "<a class='task_ops edit_task' href='#'>Edit</a>";
        delete_link = "<a class='task_ops delete_task' href='#'>Delete</a>";
        task_id_input = "<input type='hidden' class='task_id' value='"+task_id+"' />";
        task_title_input = "<input type='hidden' class='task_title' value='"+task_title+"' />";
        return edit_link+delete_link+task_id_input+task_title_input;
    };
};

var util = new Util();

Task_table_handler = function() {
    this.task_table = null;
    var _this = this;

    this.get_task_table = function() {
      return this.task_table;  
    };

    this.attach_ops_handlers = function() {
        $('#task_list').find('.edit_task').click(function() {
                                                     alert("will edit "+$(this).parent().find('input.task_id').val());
                                                     return false;
                              });
        
        $('#task_list').find('.delete_task').click(function() {
                                                       $('input#delete_id').val($(this).parent().find('input.task_id').val());
                                                       confirmation_msg = "Delete '"+$(this).parent().find('input.task_title').val()+"' ?";
                                                       $('span#delete_confirmation_msg').text(confirmation_msg);
                                                       $(this).parent().parent().addClass('selected');
                                                       $('#dialog_confirm_delete').dialog('open');
                                                       return false;
                            });        
    };
    
    this.load_task_table = function(tasks) {
        tableData = new Array();
        for(task in tasks) {
            taskData = tasks[task];
            taskArray = new Array(
                util.create_task_link(taskData['id'], taskData['title']),
                taskData['created_date'], 
                taskData['due_date'],
                taskData['assigned_to']['username'],
                taskData['state'],
                util.create_ops_links(taskData['id'], taskData['title'])
            );
            tableData.push(taskArray);
        }

        tableColumns = [
	    { "sTitle": "Task" },
	    { "sTitle": "Start Date", "sClass": "center"},
	    { "sTitle": "Due Date", "sClass": "center" },
	    { "sTitle": "Assigned To", "sClass": "center"},
	    { "sTitle": "State"},
            { "sTitle": "Operations", "sClass": "center"}
	];
        
        _this.task_table = $('#task_list').dataTable({
		                                         "aoColumns": tableColumns,
		                                         "aaData": tableData,
                                                         "iDisplayLength": 5,
                                                         "sPaginationType": "full_numbers"
	                                             });	
        _this.attach_ops_handlers();

       
    };

    this.update_task_table = function(title, created_date, due_date, assigned_to, state, ops_links) {
        _this.task_table.fnAddData([title, created_date, due_date, assigned_to, state, ops_links]);
        _this.attach_ops_handlers();
    };

};

var task_table_handler = new Task_table_handler();


init_dialogs = function() {

    save_task_click_handler = function() {
        post_data = {
            title: $('#new_task_title').val(),
            description: $('#new_task_desc').val(),
            belongs_to_project: $('#belongs_to_project').val(),
            due_date: $('#new_task_due_date').val(),
            created_date: $('#new_task_created_date').val(),
            state: $('#new_task_state').val(),
            assigned_to: $('#new_task_assigned_to option:selected').attr('id')
        };

        ajax_success_handler = function(data, textStatus, XMLHttpRequest) {
            task_id = data.split(' ')[1];
            task_table_handler.update_task_table(
                util.create_task_link(task_id, 
                                      $('#new_task_title').val()),
                $('#new_task_created_date').val(), 
                $('#new_task_due_date').val(),
                $('#new_task_assigned_to option:selected').text(),
                $('#new_task_state').val(),
                util.create_ops_links(task_id, $('#new_task_title').val())
            );

	    $('#dialog_add_task').dialog('close');                           
        };
        
        $.ajax({
                   url: '/api/projects/tasks/',
                   type: 'POST',
                   contentType: 'application/json',
                   data: JSON.stringify(post_data),
                   success: ajax_success_handler,
                   error: function(obj, text, error) {
                       alert(text);
		       $('#dialog_add_task').dialog('close');
                   }
               });        
    };

    $('#dialog_add_task').dialog({
                                     autoOpen: false,
			             height: 500,
			             width: 300,
			             modal: true,
                                     buttons: {
                                         'Save Task': save_task_click_handler,
                                         Cancel: function() {
					     $(this).dialog('close');
				         }
                                     },
                                     close: function() {
                                         $('#new_task_title').val('');
                                         $('#new_task_desc').val('');
			             }

                                 });

    $("#dialog_confirm_delete").dialog({
                                           autoOpen: false,
			                   resizable: false,
			                   height:200,
			                   modal: true,
			                   buttons: {
				               'Delete': function() {
                                                   $.ajax({
                                                              url: "/api/projects/tasks/"+$('input#delete_id').val()+"/",
                                                              type: 'DELETE',
                                                              success: function(data, textStatus) {
                                                                  var row = $("tr.selected").get(0);
                                                                  task_table = task_table_handler.get_task_table();
                                                                  task_table.fnDeleteRow(task_table.fnGetPosition(row));

                                                              }
                                                          });

                                                   $(this).dialog('close');
				               },
				               Cancel: function() {
					           $(this).dialog('close');
				               }
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
                   url: "/api/projects/"+project_id+"/tasks",
	           type: 'GET',
                   dataType: 'json',
                   timeout: 5000,
                   success: task_table_handler.load_task_table
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
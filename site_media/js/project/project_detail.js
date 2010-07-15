load_tasks = function() {
    $.ajax({
        url: "/api/projects/1/tasks",
	type: 'GET',
        dataType: 'json',
        timeout: 5000,
        success: function(tasks) {
            html = "";
            for(i=0; i<tasks.length; i++) {
                html += "<h3><a href='#'>"+tasks[i]['title']+"</a></h3><div>"+tasks[i]['description']+"</div>";
            }
            $('#task_list').html(html).accordion();
        },
    });
};

init_dialogs = function() {
    $('#dialog_add_task').dialog({
                                     autoOpen: false,
			             height: 300,
			             width: 350,
			             modal: true,
                                     buttons: {
                                         'Add Task': function() {

                                             post_data = {
                                                 title: $('#new_task_title').val(),
                                                 description: $('#new_task_desc').val(),
                                                 belongs_to_project: $('#belongs_to_project').val(),
                                             }
                                             
                                             $.ajax({
                                                        url: '/api/projects/tasks/',
                                                        type: 'POST',
                                                        contentType: 'application/json',
                                                        data: JSON.stringify(post_data),
                                                        username: 'rahuljha',
                                                        password: 'Rahul222486',
                                                        success: function(retval) {
                                                            alert(retval.toSource());
                                                        },
                                                        error: function(obj, text, error) {
                                                            alert(text);
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
}

init_buttons = function() {
    $('#add_task').click(function() {
                             $('#dialog_add_task').dialog('open');
                             return false;
});
}

$(document).ready(
    function() {
        load_tasks();
        init_dialogs();
        init_buttons();
    }
);
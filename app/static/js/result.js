/**
 * Created by malfatti on 22/02/17.
 */

         // process the form
        $('#getResult').click(function(event) {

            // get the form data
            var data = {
                'datetime'    : $('input[name=datetime]').val()
            };

            // process the form
            $.ajax({
                type        : 'GET', // define the type of HTTP verb we want to use (POST for our form)
                url         : 'result', // the url where we want to POST
                data        : data, // our data object
                dataType    : 'json', // what type of data do we expect back from the server
                encode          : true
            })
            .done(function(data) {
                $('.alert-result').text(data);
            });

            // stop the form from submitting the normal way and refreshing the page
            event.preventDefault();
        });
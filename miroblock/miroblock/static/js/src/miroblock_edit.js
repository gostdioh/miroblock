function MiroXBlockEdit(runtime, element) {
    $(element).find('.save-button').bind('click', function() {
      var handlersubmit = runtime.handlerUrl(element, 'studio_submit');
      var data = {
        bearer: $(element).find('input[name=bearer]').val()
      };

      var datastr =JSON.stringify(data)
      //runtime.notify('save', {state: 'start'});
      alert(datastr)
      $.post(handlersubmit, datastr).done(function(response) {
      console.log(response)
      //runtime.notify('save', {state: 'end'});
      });
    });
  
    $(element).find('.cancel-button').bind('click', function() {
      runtime.notify('cancel', {});
    });


    function showresult(result) {

        alert(result.result);

       // $('.count', element).text(result.count);
    }

    var handlerUrl = runtime.handlerUrl(element, 'add_board');
    $(element).find('.create-button').bind('click',  function() {
      
     
      $.post(handlerUrl, "{}").done(showresult)

     
    });


  }
  
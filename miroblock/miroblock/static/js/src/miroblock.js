/* Javascript for MiroXBlock. */
function MiroXBlock(runtime, element) {

    function updateCount(result) {
        console.log(result)
        
    }

    var handlerUrl = runtime.handlerUrl(element, 'upload_contribution');

    $('p', element).click(function(eventObject) {
        $.ajax({
            type: "POST",
            url: handlerUrl,
            data: JSON.stringify({"hello": "world"}),
            success: updateCount
        });
    });

    $(function ($) {
        /* Here's where you'd do things on page load. */
    });
}

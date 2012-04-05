$(function(){
    // Function to activate the tab
    function activateTab() {
        var activeTab = $('[href=' + window.location.hash.replace('/', '') + ']');
        activeTab && activeTab.tab('show');
    }

    // Trigger when the page loads
    activateTab();

    // Trigger when the hash changes (forward / back)
    $(window).hashchange(function(e) {
        activateTab();
    });

    // Change hash when a tab changes
    $('a[data-toggle="tab"], a[data-toggle="pill"]').on('shown', function () {
        window.location.hash = '/' + $(this).attr('href').replace('#', '');
    }); 
});


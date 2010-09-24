/***************************
	  CUSTOM JQUERY
***************************/

// FUNCTIONS

// Fix height of the Container

    var calcContainerHeight = function() {
        var headerDimensions = $('#header').height();
        $('#container').height($(window).height() - headerDimensions);
    }
  
// Fix height of Content section

    var calcContentHeight = function() {
        var headerDimensions = $('#header').height();
		var subheaderDimensions = $('#subheader').height();
        $('#content').height($(window).height() - headerDimensions - subheaderDimensions -1);
    }
  
// Make sure the whole of the sidebar menu is always displayed

	var calcSidebarHeight = function() {
		var buttonDimensions = $('a.menu').outerHeight();
		var navigationDimensions = $('ul.navigation.visible').outerHeight();
		$('div#sidebar').css('min-height', buttonDimensions + navigationDimensions+ 50);
	}
	
// Message box height compared to browser window height

	var calcMessageBox = function() {
			$('#facebox .content').height($(window).height() -250);
	}
	
// Set up sidebar menu basics

	var SidebarMenu = function() {
		if( $('ul.navigation li.current').length>0 ){
			var CurrentNavigation = $('html').find('ul.navigation li.current').parent().attr('id');
			var CurrentNavigationName = $('a[href="'+CurrentNavigation+'"]').html();
			$('a.menu').empty().append(CurrentNavigationName);
			$('ul.navigation').hide();
			$('ul.navigation li.current').parent().addClass('visible').show();
		}
		else{
			var FirstNavigation = $('html').find('ul.navigation:first').attr('id');
			var FirstNavigationName = $('a[href="'+FirstNavigation+'"]').html();
			$('ul#'+FirstNavigation).addClass('current');
			$('a.menu').empty().append(FirstNavigationName);
			$('ul.navigation:not(.current)').hide();
		}
		$('ul.navigation li ul').hide(); //Hide all sub nav's
		if( $('ul.navigation li.current:contains(ul)')){
			$('ul.navigation li.current ul').show();
		}
	}
	
// MAIN JQUERY
  
$(document).ready(function() {
	
	// Run functions on window load, and resize
	
	    $(window).resize(function() {
	        calcContainerHeight();
			calcContentHeight();
			calcMessageBox();
	    }).load(function() {
	        calcContainerHeight();
			calcContentHeight();
			SidebarMenu();
			calcSidebarHeight();
	    });
		
	// Make dropdown menu work on click
		
		$('a.menu').click(function () { 
	    	$('ul#menu').slideDown('fast'); 
			return false;
	    });
		
	// Hide dropdown when user clicks outside of it
	
		$('body').click(function() {
			$('ul#menu:visible').hide(); 
		});
		
	// Display the correct menu when picked from dropdown menu
	
		$('ul#menu li a').click(function (){
			$('ul#menu:visible').hide(); 
			var NavigationDestination = $(this).attr('href');
			if( $('ul#'+NavigationDestination).is(':visible') ) {
			}
			else{
				$('a.menu').empty().append(NavigationDestination);
				$('ul.navigation').hide();
				$('ul#'+NavigationDestination).slideDown('fast', function() {
					calcSidebarHeight();
				});
			}
			return false;
		});
		
	// If sub navigation exists, display when the link is clicked, if it's already visible do nothing, if there is no sub navigation, the link functions normally
	
		$('ul.navigation li a').not('ul.navigation li ul li a').click(function (){
			if($(this).siblings('ul:not(:visible)').length){
		    	$('ul.navigation li ul').slideUp('medium');
		    	$(this).siblings('ul').slideDown('medium', function(){
					calcSidebarHeight();
				});
		    	return false;
		    }
			else if ($(this).siblings('ul:visible').length){
				return false;
			}
			else{
		    	// Maybe do some more stuff in here...
		    }
		});
		
	// Fire the Uniform Script if checkboxes, radio buttons, or file inputs are found
	
		var applyUniform = function() {
			$.getScript('/media/js/jquery.uniform.min.js', function() {
				$("input:checkbox, input:radio, input:file").uniform();	
				$('input:file').after('<div class="clear"></div>')
        	});
		}
							
		if ($('input:checkbox').length > 0){
			applyUniform();
		}
		else if ($('input:radio').length > 0){
			applyUniform();
		}
		else if ($('input:file').length > 0){
			applyUniform();
		}
		
	
		
	// Make the facebox modal plugin run if a link is found (used for profile messages)
		
		if ($('a[rel*=facebox]')){
			$.getScript('/media/js/facebox.js', function() {
				$('a[rel*=facebox]').facebox();
				calcMessageBox();
			});
		}
		
	// Close notifications (fade and slideup)
		
		$(".notification a.close").click(function () {
			$(this).parent().fadeTo(400, 0, function () {
				$(this).slideUp(200);
			});
			return false;
		});
		
	// Apply table sorter if a table with class tablesorter is found ( in the examples case, dont sort column 1 or 5)
		
		if ($('table.tablesorter')) {
			$.getScript('/media/js/jquery.tablesorter.min.js', function() {
				$("table.tablesorter").tablesorter({
					headers: {
					}
				});
			});
		}
		
	// Check all checkboxes in the table when the header checkbox is selected
	
		$('table.tablesorter thead input[type=checkbox]').click(function(){
			var table = $(this).parents('table');
			if($(this).is(':checked')){
				table.find('div.checker span').addClass('checked');
				table.find('input[type=checkbox]').attr('checked', true);
			}
			else if($(this).is(':not(:checked)')){
				table.find('div.checker span').removeClass('checked');
				table.find('input[type=checkbox]').attr('checked', false);
			}
		});
		
		
	// Textarea limiter

		if ($('textarea.limit').length > 0){
			$.getScript('/media/js/jquery.limit-1.2.js', function() {
				$('textarea.limit').limit('150','#charsLeft');
			});
		}
		
	// Fire Color picker if input[type=color] is found

		if ($('input[type=color]').length > 0){
			$.getScript('/media/js/mColorPicker_min.js');
		}
	
  	
});

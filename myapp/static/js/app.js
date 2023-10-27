
function ajaxCall() {
    this.send = function(data, url, method, success, type) {
        type = 'json';
        var successRes = function(data) {
            success(data);
        }

        var errorRes = function(xhr, ajaxOptions, thrownError) {
            
            console.log(thrownError + "\r\n" + xhr.statusText + "\r\n" + xhr.responseText);

        }
        jQuery.ajax({
            url: url,
            type: method,
            data: data,
            success: successRes,
            error: errorRes,
            dataType: type,
            timeout: 60000
        });

    }

}

function locationInfo() {
    // var rootUrl = "https://staginglink.org/bumpload_web/api_get_state_wise_city";
    var rootUrl = "https://geodata.phplift.net/api/index.php";
    // var rootUrl = "https://www.universal-tutorial.com/api/getaccesstoken"
    // var rootUrl = "https://restcountries.com/v2/all"
    // var rootUrl = "https://www.universal-tutorial.com/api/countries/"
    var call = new ajaxCall();



    this.getCities = function(id) {
        jQuery(".cities option:gt(0)").remove();
        //get additional fields
        
        var url = rootUrl+'?type=getCities&countryId='+ '&stateId=' + id;
        var method = "post";
        var data = {};
        jQuery('.cities').find("option:eq(0)").html("Please wait..");
        call.send(data, url, method, function(data) {
            jQuery('.cities').find("option:eq(0)").html("Select City");
                var listlen = Object.keys(data['result']).length;

                if(listlen > 0)
                {
                    jQuery.each(data['result'], function(key, val) {

                        var option = jQuery('<option />');
                        option.attr('value', val.name).text(val.name);
                        jQuery('.cities').append(option);
                    });
                }
                

                jQuery(".cities").prop("disabled",false);
            
        });
    };

    this.getStates = function(id) {
        jQuery(".states option:gt(0)").remove();
        jQuery(".cities option:gt(0)").remove();
        //get additional fields
        var stateClasses = jQuery('#stateId').attr('class');

        
        var url = rootUrl+'?type=getStates&countryId=' + id;
        var method = "post";
        var data = {};
        jQuery('.states').find("option:eq(0)").html("Please wait..");
        call.send(data, url, method, function(data) {
            jQuery('.states').find("option:eq(0)").html("Select State");
            
                jQuery.each(data['result'], function(key, val) {
                    var option = jQuery('<option />');
                    option.attr('value', val.name).text(val.name);
                    option.attr('stateid', val.id);
                    jQuery('.states').append(option);
                });
                jQuery(".states").prop("disabled",false);
            
        });
    };

    this.getCountries = function() {
        var url = rootUrl+'?type=getCountries';
        var method = "post";
        var data = {};
        jQuery('.countries').find("option:eq(0)").html("Please wait..");
        call.send(data, url, method, function(data) {
            jQuery('.countries').find("option:eq(0)").html("Select Country");
            
            jQuery.each(data['result'], function(key, val) {
                var option = jQuery('<option />');
                
                option.attr('value', val.name).text(val.name);
                option.attr('countryid', val.id);
                
                jQuery('.countries').append(option);
            });
                // jQuery(".countries").prop("disabled",false);
        });
    };

}

jQuery(function() {
    var loc = new locationInfo();
    loc.getCountries();
    jQuery(".countries").on("change", function(ev) {
        var countryId = jQuery("option:selected", this).attr('countryid');
        if(countryId != ''){
            loc.getStates(countryId);
        }
        else{
            jQuery(".states option:gt(0)").remove();
        }
    });
    jQuery(".states").on("change", function(ev) {
        var stateId = jQuery("option:selected", this).attr('stateid');
        if(stateId != ''){
            loc.getCities(stateId);
        }
        else{
            jQuery(".cities option:gt(0)").remove();
        }
    });
});

$('.update_function').click(function(id){

    var rootUrl = "https://geodata.phplift.net/api/index.php";
    var callto = new locationInfo();
   var selectecountry = '';
     selectecountry = $(this).data('country');
    var selected_State = '';
    selected_State =  $(this).data('state'); 
    var city_selectted= ''
    city_selectted =  $(this).data('city');
  
  //var loadcountry =  $(".countries").val(selectecountry);
  var loadcountry =   $(".countries option[value="+selectecountry+"]").prop("selected", true);
  //alert(loadcountry);
  var loadcountrylevel = loadcountry.attr("countryid");
  var url = rootUrl+'?type=getStates&countryId=' + loadcountrylevel;
 
var statelevel = ''
  console.log('url',url);
  var call = new ajaxCall();
        var method = "post";
        var data = {};
        jQuery('.states').find("option:eq(0)").html("Please wait..");
        call.send(data, url, method, function(data) {
            jQuery('.states').find("option:eq(0)").html("Select State");
            
            jQuery.each(data['result'], function(key, val) {
                var option = jQuery('<option />');
                option.attr('value', val.name).text(val.name);
                option.attr('stateid', val.id);
                jQuery('.states').append(option);
                console.log('selected_State',selected_State);
              
               $(".states option[value='" + selected_State + "']").prop("selected", true);
              
            //    console.log('vtest', selected_State);
              var selected_state_value =    $(".states option[value='" + selected_State + "']").prop("selected", true);
               statelevel = $(".states option[value='" + selected_State + "']").attr('stateid');
               // console.log(statelevel);
               
            jQuery(".states").prop("disabled",false);
        });
        
       
   
     
         var url2 = rootUrl+'?type=getCities&countryId='+ '&stateId=' + statelevel;
         console.log(url2);
         var method = "post";
         var data = {};
         jQuery('.cities').find("option:eq(0)").html("Please wait..");
         call.send(data, url2, method, function(data) {
             jQuery('.cities').find("option:eq(0)").html("Select City");
                 var listlen = Object.keys(data['result']).length;
 
                 if(listlen > 0)
                 {
                     jQuery.each(data['result'], function(key, val) {
 
                         var option = jQuery('<option />');
                         option.attr('value', val.name).text(val.name);
                         jQuery('.cities').append(option);
                     });
                 }
                 
                
                 console.log('city_selectted',city_selectted);   
                 $(".cities option[value="+city_selectted+"]").prop("selected", true);

                 jQuery(".cities").prop("disabled",false);
             
         });
    });
})

$('#add_new_button').click(function(){ 
   // $(".states option[value='Select Country']")
   $(".countries").prop("selectedIndex", 0);
   $(".states").prop("selectedIndex", 0);
   $(".cities").prop("selectedIndex", 0);
   // $(".states")[0].selectedIndex = 0;
});

$('#empresa_session').on('change', function() {
        //alert("Entro" ); // or $(this).val()
        var id=$("#empresa_session option:selected").val();
        var value=$("#empresa_session option:selected").text();
        //alert(id); 
            $.ajax({
                url: "/config/modificarEmpresa/", // the endpoint
                type : "POST", // http method
                data : { id : id,'csrfmiddlewaretoken': '{{ csrf_token }}',texto : value }, 
                success:function(data){
                  alert("Esta trabajando con la empresa "+data);
                  
                },
                error: function(){
                  alert( "Escoja una empresa");
                },
              });
      });

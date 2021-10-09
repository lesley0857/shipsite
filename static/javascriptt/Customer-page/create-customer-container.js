        fn1 = function(name){

               console.log(name)

           $.ajax({
           type:'GET',
           url:'http://127.0.0.1:8000/create_cust_container/'+name+'/',
           data:{'mes':'xup'},
             success:function(){
                 console.log('cool')}

    })
    }

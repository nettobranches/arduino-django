Vue.component('image-cmp',{
    template:"#image-cmp",
    data:function(){
        return {
          files:[]
        }},
    methods:{
         /*
        Adds a file
      */
      addFiles(){
        this.$refs.files.click();
      },
      /*
        Submits files to the server
      */
      submitFiles(csrf_token){
        console.log('csrf_token', csrf_token);
        /*
          Initialize the form data
        */
        let formData = new FormData();
        /*
          Iteate over any file sent over appending the files
          to the form data.
        */
        for( var i = 0; i < this.files.length; i++ ){
          let file = this.files[i];
          formData.append('files[' + i + ']', file);
        }
        /*
          Make the request to the POST /select-files URL
        */
        axios.post( '/analisis_img/upload',
          formData,
          {
            headers: {
                'Content-Type': 'multipart/form-data'
            },
            data:{
                csrfmiddlewaretoken: csrf_token
            }
          }
        ).then(function(){
          console.log('SUCCESS!!');
        })
        .catch(function(){
          console.log('FAILURE!!');
        });
      },
      /*
        Handles the uploading of files
      */
      handleFilesUpload(){
        let uploadedFiles = this.$refs.files.files;
        /*
          Adds the uploaded file to the files array
        */
        for( var i = 0; i < uploadedFiles.length; i++ ){
          this.files.push( uploadedFiles[i] );
        }
      },
      /*
        Removes a select file the user has uploaded
      */
      removeFile( key ){
        this.files.splice( key, 1 );
      }
    } // methods
}); // component cliente

Vue.component('singlefile',{
    template:"#singlefile",
    data:function(){
        return {
          file:''
        }},
    methods:{
      /*
        Submits the file to the server
      */
      submitFile(csrf_token){
        console.log('csrf_token', csrf_token);
        /*
                Initialize the form data
            */
            let formData = new FormData();

            /*
                Add the form data we need to submit
            */
            //formData.append('file', this.file);

        /*
          Make the request to the POST /single-file URL
        */
            axios.post( '/analisis_img/upload',
                formData,
                {
                headers: {
                    'Content-Type': 'multipart/form-data'
                },
                  data:{
                      csrfmiddlewaretoken: csrf_token
                  }
              }
            ).then(function(){
          console.log('SUCCESS!!');
        })
        .catch(function(){
          console.log('FAILURE!!');
        });
      },

      /*
        Handles a change on the file upload
      */
      handleFileUpload(){
        this.file = this.$refs.file.files[0];
      }
    } // methods
}); // component cliente


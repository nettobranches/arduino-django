Vue.component('image-cmp',{
    template:"#image-cmp",
    data:function(){
        return {
            port: "COM4",

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
      submitFiles(){
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
        axios.post( '/select-files',
          formData,
          {
            headers: {
                'Content-Type': 'multipart/form-data'
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


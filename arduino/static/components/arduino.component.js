Vue.component('arduino-uno',{
    template:"#arduino-uno",
    data:function(){
        return {
            port: "COM4",
            tipo: "",
            idx: "",
            mode: "",
            value: "",
            timer: null,
            timerTime: 100,
            analogPins: [],
            digitalPins: []

        }},
    methods:{
        init: function(){
            axios.get('/arduino/init/'+this.port)
            .then(function (response) {
                // handle success
                console.log(response);
            })
            .catch(function (error) {
                // handle error
                console.log(error);
            })
        } // init
        ,startPin: function(){
            var _this = this;

            if(this.tipo == 'a'){
                this.startAnalogPin()
            }else if(this.tipo == 'd'){
                this.startDigitalPin()
            }
        } // get
        ,startAnalogPin: function(){
            var _this = this;

            axios.get('/arduino/start_analog/'+this.idx+'/'+this.mode)
            .then(function (response) {  
            // handle success
                _this.analogPins.push({idx: _this.idx, mode: _this.mode})
                console.log(response);
            })
            .catch(function (error) {
            // handle error
            console.log(error);
            })
        } // get
        ,startDigitalPin: function(){
            var _this = this;

            axios.get('/arduino/start_digital/'+this.idx+'/'+this.mode)
            .then(function (response) {
                _this.digitalPins.push({tipo:"d", idx: _this.idx, mode: _this.mode})
            // handle success
            console.log(response);
            })
            .catch(function (error) {
            // handle error
            console.log(error);
            })
        } // get
        ,set: function(){
            var _this = this;
            
        } // set
        ,get: function(pin){
            var _this = this;
            axios.get('/arduino/get_analog_val/'+pin.idx)
            .then(function (response) {
            // handle success
            console.log(response);
            })
            .catch(function (error) {
            // handle error
            console.log(error);
            })
        } // get
        ,get_d: function(pin){
            var _this = this;
            axios.get('/arduino/get_digital_val/'+pin.idx)
            .then(function (response) {
            // handle success
            console.log(response);
            })
            .catch(function (error) {
            // handle error
            console.log(error);
            })
        } // get
        ,start_monitor: function(){
            var _this = this;
            this.timer = setInterval(function(){
                _this.get();
            }, this.timerTime);
            
        } // start_monitor
        ,stop_monitor: function(){
            var _this = this;
            clearTimeout(this.timer);
            
        } // stop_monitor
        ,start_servo: function(){
            var _this = this;
            axios.get('/arduino/start_servo/')
            .then(function (response) {
            // handle success
            console.log(response);
            })
            .catch(function (error) {
            // handle error
            console.log(error);
            })
        }
        ,move_servo: function(deg){
            var _this = this;
            axios.get('/arduino/move_servo/'+deg)
            .then(function (response) {
            // handle success
            console.log(response);
            })
            .catch(function (error) {
            // handle error
            console.log(error);
            })
        }
    } // methods
}); // component cliente
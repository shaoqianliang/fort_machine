String.prototype.Format = function(arg){

        var temp = this.replace(/\{(\w+)\}/g,function(k,kk){
            return arg[kk];
        });
        return temp;
        };
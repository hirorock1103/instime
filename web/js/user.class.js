class User {

    id = "";
    instime_name = "";
    instime_id = "";
    instime_pw = "";


    //SETTER
    setId(id){
        this.id = id;
    }
    setInstimeName(instime_name){
        this.instime_name = instime_name;
    }
    //GETTER
    getInstimeName(){
        return this.instime_name;
    }
    getId(){
        return this.id;
    }

}
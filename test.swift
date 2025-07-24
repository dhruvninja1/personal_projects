class person {
    var name: String
    var age: Int


    init(name: String, age: Int){
        self.name = name
        self.age = age
    }

    func introduce(){
        print("Hi I am \(name) and I am \(age) years old")
    }

}



let Dhruv: person = person(name: "Dhruv", age: 12)

Dhruv.introduce()
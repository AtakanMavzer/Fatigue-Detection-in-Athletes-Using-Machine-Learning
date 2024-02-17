const supertest = require('supertest');
const app = require('./backend/server');

describe("POST /users",()=>{
  
  describe("given a login info",()=>{
    it("should return a token", ()=>{
      const res=supertest(app)
      .post("/api/users/login")
      .send({
        email: "ab",
        password: "12345"
      })//print the response
      
      
    })
  })
})


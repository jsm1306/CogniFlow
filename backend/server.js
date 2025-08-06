import express from 'express'
import dotenv from 'dotenv'
dotenv.config()
const app=express() 
app.use((req,res,next) => {
    console.log(req.path,req.method)
    next()
   })
app.get('/',(req,res) => {
 res.json({mssg: "Welcome to the app"})
})
app.listen(process.env.PORT, () => {
 console.log('Listening on port', process.env.PORT)
})

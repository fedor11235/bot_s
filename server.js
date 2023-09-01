import express from 'express'
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()
const app = express()
const port = 3001

app.get('/promocode', async  (req, res) => {
  const idUser = req.query.id
  const promocode = String(new Date().valueOf())
  await prisma.promoCode.create({
    data: { 
      idUser: idUser,
      code: promocode
    },
  });
  res.send(promocode)
})

app.get('/create-chanel', async  (req, res) => {
  const idUser = req.query.idUser
  const idChanel = req.query.idChanel
  const isUserChanel = await prisma.userChanel.findFirst({
    where: {
      idUser: idUser,
      idChanel: idChanel
    },
  });
  if(isUserChanel) {
    res.send('exist')
    return
  }
  await prisma.userChanel.create({
    data: { 
      idUser: idUser,
      idChanel: idChanel
    },
  });
  await prisma.User.create({
    data: { 
      idUser: idUser,
    },
  });
  res.send('created')
})

app.get('/check', async  (req, res) => {
  const idUser = req.query.idUser
  const isUserChanel = await prisma.userChanel.findFirst({
    where: {
      idUser: idUser,
    },
  });
  if(isUserChanel) {
    res.send('exist')
    return
  }
  res.send('empty')
})

app.get('/profile', async  (req, res) => {
  const idUser = req.query.idUser
  const user = await prisma.user.findFirst({
    where: {
      idUser: idUser,
    },
  });
  console.log('user', user)
  res.send({
    tariffPlan: user.tariffPlan,
    subscriptionEndDate: user.subscriptionEndDate,
    createdOpt: user.createdOpt,
    byOpt: user.byOpt,
    totalSavings: user.totalSavings,
    invitedUsers: user.invitedUsers,
    totalEarned: user.totalEarned,
    channels: user.channels,
  })
})

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})
import express from 'express'
import request from 'request';
import { PrismaClient } from '@prisma/client'

const token = '746c997297440937501f953ec01c985f'
const prisma = new PrismaClient()
const app = express()
const port = 3001
const categoriesUrl = `https://api.tgstat.ru/database/categories?token=${token}`
const categoriesList = ['education', 'health', 'news', 'tech', 'entertainment', 'psychology', 'other']
// const categoriesList = ['education']

function getUrlCategoriesTop(category, limit) {
  return `https://api.tgstat.ru/channels/search?token=${token}&category=${category}&limit=${limit}&country=ru`
}

function getUrlCategoryStat(username) {
  return `https://api.tgstat.ru/channels/stat?token=${token}&channelId=${username}`
}

function getCategoriesTop() {
  for(const category of categoriesList) {
    const urlCategoriesTop = getUrlCategoriesTop(category, 30)

    // request({url: urlCategoriesTop, json: true}, (error, response, data) => {
    //   const chanelsTop = data.response;
    //   for(const chanel of chanelsTop.items) {
    //     const urlCategoryStat = getUrlCategoryStat(chanel.username)
    //     request({url: urlCategoryStat, json: true}, async (error, response, data) => {
    //       const categoryStat = data.response;
    //       if(categoryStat) {
    //         const catalogNew = await prisma.catalog.create({
    //           data: { 
    //             category: category,
    //             username: chanel.username,
    //             title: chanel.title,
    //             daily_reach: categoryStat.daily_reach,
    //             ci_index: categoryStat.ci_index,
    //             participants_count: categoryStat.participants_count,
    //             avg_post_reach: categoryStat.avg_post_reach,
    //             forwards_count: categoryStat.forwards_count,
    //           },
    //         });
    //       }
    //     });
    //   }
    // });
    
  }
}

app.get('/category', async  (req, res) => {
  const categoryQuery = req.query.category
  let categoryFind
  if(categoryQuery === 'all') {
    categoryFind = await prisma.catalog.findMany();
  } else {
    categoryFind = await prisma.catalog.findMany({
      where: {
        category: categoryQuery,
      }
    });
  }
  res.send(categoryFind)
})

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
  getCategoriesTop()
})

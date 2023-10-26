// const chatId = '-1001959790816'
const chatId = '6339441025'

// Тестовый бот
const botToken = '6127498929:AAEYlTDQQ2XsmFfRNtqIc8kpZUNLTzSrLB8'
// Продовский бот
// const botToken = '6569483795:AAGXGV2Awd_fVhgy_20sjDpdfGJMaf6Ex6w'
const message_edit = '791'
const text = 'Новое сообщение'

// editMessageText
// sendMessage

const data = {
  chat_id: chatId,
  message_id: message_edit,
  text: text,
}

fetch(`https://api.telegram.org/bot${botToken}/editMessageText`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify(data),
}).then((res) => {
  console.log(res.status)
})

// fetch(`https://api.telegram.org/bot${botToken}/sendMessage`, {
//   method: "POST",
//   headers: {
//     "Content-Type": "application/json",
//   },
//   body: JSON.stringify(data),
// }).then((res) => {
//   console.log(res.status)
// })

// fetch(`https://api.telegram.org/bot${botToken}/getUpdates`, {
//   method: "POST",
//   headers: {
//     "Content-Type": "application/json",
//   },
//   body: JSON.stringify(data),
// }).then((res) => {
//   console.log(res.status)
// })

// fetch(`https://api.telegram.org/bot${botToken}/sendMessage?chat_id=${chatId}&text=${text}`).then((res) => {
//   console.log(res.status)
// })
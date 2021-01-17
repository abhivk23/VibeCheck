const TO_NUMBER = 12012852125
const VONAGE_NUMBER = 14252330889

const app = require('express')()
const bodyParser = require('body-parser')

app.use(bodyParser.json())

const onInboundCall = (request, response) => {
  const ncco = [{
      action: "record",
      eventUrl: [`${request.protocol}://${request.get('host')}/webhooks/recordings`]
    },
    {
      action: "connect",
      from: VONAGE_NUMBER,
      endpoint: [{
        type: "phone",
        number: TO_NUMBER
      }]
    }
  ]
  response.json(ncco)
}

const onRecording = (request, response) => {
  const recording_url = request.body.recording_url
  console.log(request.body)
  console.log(`Recording URL = ${recording_url}`)

  response.status(204).send()
}

app
  .get('/webhooks/answer', onInboundCall)
  .post('/webhooks/recordings', onRecording)

app.listen(3000)
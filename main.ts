input.onButtonPressed(Button.A, function () {
    led.enable(false)
    basic.clearScreen()
    while (input.buttonIsPressed(Button.B) == false && input.buttonIsPressed(Button.AB) == false) {
        serial.writeValue("x", input.acceleration(Dimension.X))
        serial.writeValue("y", input.acceleration(Dimension.Y))
        serial.writeValue("z", input.acceleration(Dimension.Z))
    }
})
input.onButtonPressed(Button.AB, function () {
    basic.clearScreen()
})
input.onButtonPressed(Button.B, function () {
    while (input.buttonIsPressed(Button.A) == false && input.buttonIsPressed(Button.AB) == false) {
        led.enable(true)
        led.plot(randint(0, 4), randint(0, 4))
        led.plot(randint(0, 4), randint(0, 4))
        led.plot(randint(0, 4), randint(0, 4))
        led.plot(randint(0, 4), randint(0, 4))
        led.plot(randint(0, 4), randint(0, 4))
        control.waitMicros(500000)
        led.enable(false)
        basic.clearScreen()
    }
})

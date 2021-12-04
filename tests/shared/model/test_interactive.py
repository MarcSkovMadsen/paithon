import panel as pn

from paithon import interactive


def test_interactive():
    # Given
    def model(value1, value2):
        return value1, value2

    input1_org = pn.widgets.TextInput
    input2_org = pn.widgets.TextInput()
    output1_org = pn.pane.Str
    output2_org = pn.pane.Str(name="Output 2")
    # When
    inputs, outputs = interactive(
        model, inputs=[input1_org, input2_org], outputs=[output1_org, output2_org]
    )
    # Then
    input1, input2 = inputs
    assert isinstance(input1, pn.widgets.TextInput)
    assert input2 == input2_org

    output1, output2 = outputs
    assert isinstance(output1, pn.pane.Str)
    assert output2 == output2_org

    input1.value = "Hello"
    output1.object == input1.value

    input2.value = "World"
    output2.object == input1.value

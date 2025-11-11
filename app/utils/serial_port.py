from PyQt6.QtSerialPort import QSerialPort, QSerialPortInfo


def get_port_names():
    portList = QSerialPortInfo.availablePorts()
    portList = sorted(portList, key=lambda port: eval(port.portName()[3:]))
    return [port.portName() for port in portList]

def get_serial_ports():
    portList = QSerialPortInfo.availablePorts()
    return [port for port in portList 
            if port.hasVendorIdentifier() 
            and port.hasProductIdentifier()
            ]

def get_port_by_name(name: str) -> QSerialPort | None:
    portList = QSerialPortInfo.availablePorts()
    for portInfo in portList:
        if portInfo.portName() == name:
            serialPort = QSerialPort(portInfo)
            return serialPort
    return None

def connect(portInfo: QSerialPortInfo, baud_rate: int) -> QSerialPort | None:
    serialPort = QSerialPort(portInfo)
    serialPort.setBaudRate(baud_rate)
    serialPort.setStopBits(QSerialPort.StopBits.OneStop)
    serialPort.setDataBits(QSerialPort.DataBits.Data8)
    serialPort.setFlowControl(QSerialPort.FlowControl.NoFlowControl)

    if not serialPort.open(QSerialPort.OpenModeFlag.ReadWrite):
        print("Serial Port Open Failed: " + serialPort.errorString())
        return None
    return serialPort

def connect_by_name(port_name: str, baud_rate: int) -> QSerialPort | None:
    serialPort = get_port_by_name(port_name)
    if serialPort is None:
        return None
    
    serialPort.setBaudRate(baud_rate)
    serialPort.setStopBits(QSerialPort.StopBits.OneStop)
    serialPort.setDataBits(QSerialPort.DataBits.Data8)
    serialPort.setFlowControl(QSerialPort.FlowControl.NoFlowControl)

    if not serialPort.open(QSerialPort.OpenModeFlag.ReadWrite):
        return None
    return serialPort
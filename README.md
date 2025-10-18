# Raspberry Pi OLED Display System Monitor

A Python application that displays real-time system information on a 128x32 I2C OLED display connected to a Raspberry Pi.
 Shows hostname, IP address, CPU usage, and memory usage with animated progress bars.

## Features

- **Real-time System Monitoring**: Displays hostname, IP address, CPU usage, and memory usage
- **Animated Progress Bars**: Visual representation of CPU and memory utilization
- **Status Indicator**: Blinking pixel in top-right corner shows the application is running
- **Multiple Deployment Options**: Supports Python virtual environment, Docker, and Docker Compose
- **Low Resource Usage**: Optimized for continuous operation on Raspberry Pi

## Hardware Requirements

### Required Components
- **SSD1306 128x32 I2C OLED Display** (0.96" or 0.91" size)
- **Raspberry Pi** (any model with I2C support)
- **Jumper wires** for connections

### Wiring Diagram
```
OLED Display   →    Raspberry Pi
VCC            →    3.3V (Pin 1)
GND            →    Ground (Pin 6 or Pin 9)
SCL            →    GPIO 3 (Pin 5) - SCL
SDA            →    GPIO 2 (Pin 3) - SDA
```

### Hardware Setup
1. **Enable I2C Interface**:
   ```bash
   sudo raspi-config
   ```
   Navigate to: `Interfacing Options` → `I2C` → `Enable`

2. **Optional: Increase I2C Speed to 1MHz**:
   Edit `/boot/config.txt` (or `/boot/firmware/config.txt` on newer Pi OS):
   ```bash
   sudo nano /boot/config.txt
   ```
   Add or modify the line:
   ```
   dtparam=i2c_arm=on,i2c_arm_baudrate=1000000
   ```
   Reboot the Raspberry Pi:
   ```bash
   sudo reboot
   ```

## Installation & Usage

### Method 1: Python Virtual Environment

**Prerequisites:**
- Python 3.x
- Git

**Setup:**
```bash
# Clone the repository
git clone https://github.com/jpflouret/rpi-display.git
cd rpi-display

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python display.py
```

### Method 2: Docker

**Prerequisites:**
- Docker installed on Raspberry Pi

**Setup:**
```bash
# Clone the repository
git clone https://github.com/jpflouret/rpi-display.git
cd rpi-display

# Build the Docker image
docker build -t rpi-display .

# Run the container
docker run --privileged --network host rpi-display
```

### Method 3: Docker Compose (Recommended)

**Prerequisites:**
- Docker Compose installed

**Setup:**
```bash
# Clone the repository
git clone https://github.com/jpflouret/rpi-display.git
cd rpi-display

# Start the service
docker compose up -d

# View logs
docker compose logs -f

# Stop the service
docker compose down
```

The Docker Compose method uses a pre-built image from `ghcr.io/jpflouret/rpi-display:latest` and automatically handles privileged mode and host networking.

### Method 4: Kubernetes DaemonSet

**Prerequisites:**
- Raspberry Pi Kubernetes cluster with nodes that have I2C/GPIO access
- `kubectl` configured to access your cluster

**Setup:**
```bash
# Clone the repository
git clone https://github.com/jpflouret/rpi-display.git
cd rpi-display

# Deploy the DaemonSet
kubectl create namespace rpi-display
kubectl apply -f daemonset.yaml -n rpi-display

# View the DaemonSet status
kubectl get daemonset rpi-display -n rpi-display

# View pods running on each node
kubectl get pods -l app.kubernetes.io/name=rpi-display -n rpi-display -o wide

# View logs from a specific pod
kubectl logs -l app.kubernetes.io/name=rpi-display -n rpi-display --tail=50

# Delete the DaemonSet
kubectl delete -f daemonset.yaml
```

**Features:**
- Automatically deploys to all nodes in the cluster (including control-plane nodes)
- Uses privileged containers for I2C/GPIO access
- Host networking for ip and hostname access
- Resource limits to prevent excessive resource usage
- Tolerations to allow scheduling on control-plane nodes

## Troubleshooting

### Common Issues

**I2C Not Enabled**
- Run `sudo raspi-config` and enable I2C interface
- Reboot the Raspberry Pi

**Display Not Detected**
- Check wiring connections
- Install the `i2c-tools` package: `sudo apt-get install i2c-tools`
- Verify I2C is enabled: `sudo i2cdetect -y 1`
- Look for device at address `0x3C` in the output

**Docker Permission Issues**
- The `--privileged` flag is required for GPIO/I2C access

## Dependencies

- `adafruit-circuitpython-ssd1306` - SSD1306 OLED display driver
- `psutil` - System and process utilities
- `RPi.GPIO` - Raspberry Pi GPIO access
- `pillow` - Image processing
- `numpy` - Numerical computing

## References

- [Adafruit CircuitPython SSD1306 Library](https://github.com/adafruit/Adafruit_CircuitPython_SSD1306)
- [Adafruit Monochrome OLED Breakouts Documentation](https://learn.adafruit.com/monochrome-oled-breakouts)
- [Raspberry Pi I2C Configuration](https://www.raspberrypi.org/documentation/configuration/raspi-config.md)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

JP Flouret

---

**Note**: This project is based on examples from the
[Adafruit CircuitPython SSD1306 library](https://github.com/adafruit/Adafruit_CircuitPython_SSD1306)
and follows the hardware documentation from
[Adafruit's OLED breakout guide](https://learn.adafruit.com/monochrome-oled-breakouts).

# Raspberry Pi Setup

This guide runs MealPlanner on a Raspberry Pi for private household use. Phones, tablets, and laptops can connect from the same home network.

## Recommended hardware

- Raspberry Pi 4 or 5
- 4 GB RAM or more
- 32 GB or larger microSD card
- Raspberry Pi OS Lite 64-bit
- Ethernet connection if available
- Reliable power supply

A Raspberry Pi 4 is sufficient for the current application. A Pi 5 provides more headroom but is not required.

## 1. Install Raspberry Pi OS

1. Install Raspberry Pi Imager on another computer.
2. Write **Raspberry Pi OS Lite (64-bit)** to the microSD card.
3. In the Imager settings, configure:
   - Hostname, for example `mealplanner`
   - Wi-Fi credentials, if Ethernet is not used
   - A secure Raspberry Pi login password
   - SSH access
4. Insert the card and start the Pi.
5. Connect over SSH:

```bash
ssh YOUR_PI_USER@mealplanner.local
```

If `.local` does not resolve, find the Pi's address in your router or use a network scanner.

## 2. Install Docker

Update the operating system:

```bash
sudo apt update
sudo apt full-upgrade -y
```

Install Docker using the official convenience script:

```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker "$USER"
```

Log out and back in, or restart the Pi, so the group change takes effect. Verify Docker:

```bash
docker --version
docker compose version
```

## 3. Download the app

Clone the repository and enter it:

```bash
git clone https://github.com/YOUR_GITHUB_USER/MealPlanner.git
cd MealPlanner
```

Replace the repository URL with the actual GitHub repository URL.

## 4. Start MealPlanner

Build and start the app in the background:

```bash
docker compose up --build -d
```

Check that the container is running:

```bash
docker compose ps
docker compose logs -f meal-planner
```

The health check should eventually report `healthy`:

```bash
docker inspect --format '{{.State.Health.Status}}' mealplanner-meal-planner-1
```

The exact container name may differ. Use `docker compose ps` if needed.

## 5. Connect from family devices

Find the Pi's local IP address:

```bash
hostname -I
```

From a phone, tablet, or laptop connected to the same home network, open:

```text
http://PI_IP_ADDRESS:8000
```

For example:

```text
http://192.168.1.50:8000
```

Open `/profile` to select a household member and configure their saved profile.

The app is currently passwordless. Anyone with access to the home network can select a family profile, so keep it private to your trusted LAN.

## 6. Give the Pi a stable address

A stable address makes the app easier to bookmark. The preferred approach is to create a DHCP reservation in the home router for the Pi's MAC address. Give it a name such as `mealplanner` and reserve its current IP.

After that, family members can bookmark the same address:

```text
http://mealplanner.local:8000
```

or:

```text
http://PI_RESERVED_IP:8000
```

## Data storage

The Compose file stores the SQLite database in the persistent Docker volume `mealplanner_meal_planner_data`, mounted inside the container at `/data`.

The database survives:

- Container restarts
- `docker compose down`
- Image rebuilds

Do not use `docker compose down -v` unless you intentionally want to delete the database volume.

## Backups

For a normal checkout with a local `meal_planner.db` file, run:

```bash
make backup
```

For the Docker volume, create a database backup inside the mounted volume:

```bash
docker compose exec meal-planner sh -c \
  'mkdir -p /data/backups && cp /data/meal_planner.db /data/backups/meal_planner-$(date +%Y%m%d-%H%M%S).db'
```

Copy a backup from the container to the Pi's current directory if needed:

```bash
docker compose cp meal-planner:/data/backups/meal_planner-YYYYMMDD-HHMMSS.db ./
```

For dependable backups, copy the backup files to another computer or external drive as well. A backup kept only on the Pi does not protect against a failed SD card.

## Updating the app

From the application directory:

```bash
git pull

docker compose up --build -d
```

The container startup command applies pending Alembic migrations before starting Uvicorn.

Check the result:

```bash
docker compose ps
docker compose logs --tail=100 meal-planner
```

## Stopping and restarting

Restart the app:

```bash
docker compose restart
```

Stop the app without deleting data:

```bash
docker compose down
```

Start it again:

```bash
docker compose up -d
```

## Troubleshooting

### The page does not open

Check the container and health endpoint:

```bash
docker compose ps
docker compose logs --tail=100 meal-planner
curl http://localhost:8000/health
```

The health endpoint should return:

```json
{"status":"ok"}
```

From another device, confirm it is on the same Wi-Fi network and use the Pi's IP address, not `localhost`.

### Port 8000 is already in use

Check what is using the port:

```bash
sudo ss -ltnp | grep ':8000'
```

To use another host port, edit Compose:

```yaml
ports:
  - "8080:8000"
```

Then connect to `http://PI_IP_ADDRESS:8080`.

### The Pi has little disk space

Inspect Docker usage:

```bash
docker system df
df -h
```

Remove unused Docker images only after checking that they are not needed:

```bash
docker image prune
```

### The database should never be reset accidentally

Do not run:

```bash
docker compose down -v
```

unless you have a verified backup and deliberately want to remove the stored data.

## Remote access warning

Do not forward port 8000 from your router to the public internet. The current local profile system has no passwords. For remote access later, add authentication and HTTPS first, then use a VPN such as Tailscale or a properly secured reverse proxy.

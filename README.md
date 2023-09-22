## Prerequisites

- [Appium](http://appium.io/docs/en/2.1/quickstart/) installed and running
- android-sdk (Install Android Studio for the easiest experience)
- Android device with USB Debugging mode (enable it in the developer setting)


## Troubleshooting

### Socket hang up
**Problem**:
```
...
selenium.common.exceptions.WebDriverException: Message: An unknown server-side error occurred while processing the command. Original error: Could not proxy command to the remote server. Original error: socket hang up
...
```

**Solution**: Try to reboot the device

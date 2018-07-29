import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.net.InetAddress;
import java.net.UnknownHostException;
import java.util.Calendar;
import java.util.Date;
import java.util.List;

import javax.imageio.ImageIO;
import javax.swing.filechooser.FileSystemView;

import au.com.southsky.jfreesane.OptionValueType;
import au.com.southsky.jfreesane.SaneDevice;
import au.com.southsky.jfreesane.SaneException;
import au.com.southsky.jfreesane.SaneOption;
import au.com.southsky.jfreesane.SaneSession;

public class Scannn {

	private static String SANE_SERVER = "localhost";
	private static String DPI_OPTION_NAME = "resolution";

	public static void main(String[] args) {
		// DPI value
		boolean test = false;
		int dpi = 0;
		if (args.length > 0) {
			try {
				if (args[0] != null && args[0].equals("test")) {
					test = true;
				} else {
					dpi = Integer.parseInt(args[0]);
				}
			} catch (Exception e) {
				System.out.println(e.toString());
			}
		}
		// RUNNN
		// Sane Daemon
		System.out.println("V1: Connecting to the Sane backend ...");
		InetAddress address = null;
		SaneSession session = null;
		try {
			address = InetAddress.getByName(Scannn.SANE_SERVER);
			if (address != null) {
				session = SaneSession.withRemoteSane(address);
				if (session != null) {
					// Devices
					System.out.println("Checking for connected devices ...");
					List<SaneDevice> devices = null;
					try {
						devices = session.listDevices();
					} catch (SaneException e) {
						e.printStackTrace();
						System.out.println(e.toString());
					}
					if (devices != null && devices.size() > 0) {
						System.out.println(devices.size() + " device"
								+ ((devices.size() > 1) ? "s" : "") + " found");
						int i = 0;
						for (SaneDevice device : devices) {
							i++;
							// Open
							if (!device.isOpen()) {
								System.out.println("Connecting ...");
								try {
									device.open();
								} catch (SaneException e) {
									e.printStackTrace();
									System.out.println(e.toString());
								}
								if (device.isOpen()) {
									// Device properties
									System.out.println("Name:" + device.getName());
									System.out.println("Model:" + device.getModel());
									System.out.println("Type:" + device.getType());
									System.out.println("Vendor:" + device.getVendor());
									if (!test) {
										// Options
										System.out.println("Options configuration ...");
										// Option
										SaneOption option = null;
										String dpiFileName = null;
										try {
											option = device.getOption(Scannn.DPI_OPTION_NAME);
											// Current value
											dpiFileName = Scannn.readDpi(device) + "";
											System.out.println(Scannn.readDpi(device) + " dpi");
											// Writable
										} catch (IOException e) {
											e.printStackTrace();
											System.out.println(e.toString());
										} catch (SaneException e) {
											e.printStackTrace();
											System.out.println(e.toString());
										}
										if (dpi > 0) {
											if (option != null && option.isActive() && option.isWriteable()) {
												// Type INT + single value
												if (option.getType() == OptionValueType.INT
														&& option.getValueCount() == 1) {
													// Constraints
													List<Integer> list = option.getIntegerValueListConstraint();
													System.out.println("values: " + list.toString());
													// New value must be in constraints list
													if (list.contains(dpi)) {
														try {
															option.setIntegerValue(dpi);
															System.out.println(dpi + " dpi");
															dpiFileName = dpi + "";
														} catch (SaneException e) {
															e.printStackTrace();
															System.out.println(e.toString());
														}
													} else {
														System.out.println("Scannn: bad dpi value");
													}
												} else {
													System.out.println("Scannn: bad dpi format...");
												}
											} else {
												System.out.println("Scannn: resolution is not writable");
											}
										}
										if (dpiFileName != null) {
											// Read from device
											System.out.println("Reading ...");
											BufferedImage image = null;
											try {
												image = device.acquireImage();
											} catch (SaneException e) {
												e.printStackTrace();
												System.out.println(e.toString());
											}
											if (image != null) {
												// Write in file
												System.out.println("Saving ...");
												// Directory
												String dirName = Scannn.getHomeDirectory();
												File dir = new File(dirName);
												if (!dir.exists()) {
													if (!dir.mkdir()) {
														//throw new Exception("Directory was not created");
													}
												}
												// Free space
												System.out.println(dir.getUsableSpace() + " bytes available");
												System.out
														.println((dir.getUsableSpace() / 1000) + " K bytes available");
												System.out.println((dir.getUsableSpace() / 1000 / 1000)
														+ " M bytes available");
												System.out.println((dir.getUsableSpace() / 1000 / 1000 / 1000)
														+ " G bytes available");
												if (dir.getUsableSpace() > 104857600) {
													// Date
													Date date = new Date();
													Calendar calendar = Calendar.getInstance();
													calendar.setTime(date);
													// Name
													String fileName = dirName + "/" + i + "_";
													fileName += calendar.get(Calendar.YEAR);
													fileName += "-";
													fileName += (calendar.get(Calendar.MONTH) + 1);
													fileName += "-";
													fileName += calendar.get(Calendar.DAY_OF_MONTH);
													fileName += "_";
													fileName += calendar.get(Calendar.HOUR_OF_DAY);
													fileName += "-";
													fileName += calendar.get(Calendar.MINUTE);
													fileName += "-";
													fileName += calendar.get(Calendar.SECOND);
													fileName += "_";
													fileName += dpiFileName;
													fileName += ".jpg";
													// File
													File file = new File(fileName);
													ImageIO.write(image, "jpg", file);
													JPEGImageWriteParam jpegParams = new JPEGImageWriteParam(null);
													jpegParams.setCompressionMode(ImageWriteParam.MODE_EXPLICIT);
													jpegParams.setCompressionQuality(1f);
													System.out.println("Saved at: " + fileName);
												} else {
													//throw new Exception("Need more free space !");
												}
											}
										}									
									} else {
										// SysO the DPI list
										try {
											Scannn.readAvailableDpi(device);
										} catch (SaneException e) {
											e.printStackTrace();
											System.out.println(e.toString());
										}
									}
								}
							} else {
								Scannn.deviceAlreadyUsed();
							}
							// Close
							if (device.isOpen()) {
								device.close();
							}
						}
					} else {
						Scannn.noDevice();
					}
					System.out.println("Bye!");
					session.close();
				} else {
					Scannn.noSaneServer();
				}
			} else {
				Scannn.noSaneServer();
			}
		} catch (UnknownHostException e) {
			e.printStackTrace();
			System.out.println(e.toString());
		} catch (IOException e) {
			e.printStackTrace();
			System.out.println(e.toString());
		}
	}

	/**
	 * Fires when no device was found
	 */
	private static void noDevice() {
		System.out.println("Scannn: No device found");
	}

	/**
	 * Fires when Sane session is null or when no Sane server was found
	 */
	private static void noSaneServer() {
		System.out.println("Scannn: Sane session is null");
	}

	/**
	 * Fires when device is already used by another process
	 */
	private static void deviceAlreadyUsed() {
		System.out.println("Scannn: Device is already used");
	}

	/**
	 * Displays the DPI list for a device
	 * 
	 * @param device
	 *            the current device
	 * @throws IOException
	 * @throws SaneException
	 */
	private static void readAvailableDpi(SaneDevice device) throws IOException,
			SaneException {
		// Option
		SaneOption option = device.getOption(Scannn.DPI_OPTION_NAME);
		// Current value
		System.out.println("Default: " + Scannn.readDpi(device) + " dpi");
		// Writable
		if (option != null && option.isActive() && option.isWriteable()) {
			// Type INT + single value
			if (option.getType() == OptionValueType.INT
					&& option.getValueCount() == 1) {
				// Constraints
				List<Integer> list = option.getIntegerValueListConstraint();
				System.out.println("values: " + list.toString());
			} else {
				System.out.println("Scannn: bad dpi format...");
			}
		} else {
			System.out.println("Scannn: resolution is not writable");
		}
	}

	/**
	 * Reads the current DPI value for a device
	 * 
	 * @param device
	 *            The device to check
	 * @throws IOException
	 * @throws SaneException
	 */
	private static int readDpi(SaneDevice device) throws IOException,
			SaneException {
		// Option
		SaneOption option = device.getOption(Scannn.DPI_OPTION_NAME);
		// Readable
		if (option != null && option.isActive() && option.isReadable()) {
			// Type INT + single value
			if (option.getType() == OptionValueType.INT
					&& option.getValueCount() == 1) {
				return option.getIntegerValue();
			} else {
				System.out.println("Scannn: bad dpi format...");
			}
		} else {
			System.out.println("Scannn: resolution is not readable");
		}
		return 0;
	}

	/**
	 * Gets the home directory's path
	 * 
	 * @return the path as String
	 */
	private static String getHomeDirectory() {
		// Home directory
		FileSystemView fsv = FileSystemView.getFileSystemView();
		String dirName = fsv.getHomeDirectory() + "";
		if (dirName == null || dirName.equals("") || dirName.equals("/")) {
			// Default location
			dirName = "/tmp";
		}
		// Sub directory
		dirName += "/scannn";
		File dir = new File(dirName);
		if (!dir.exists()) {
			dir.mkdir();
		}
		return dirName;
	}
}
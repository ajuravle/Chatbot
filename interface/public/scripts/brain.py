import aiml, sys


# Create the kernel and learn AIML files
kernel = aiml.Kernel()
kernel.learn("public/scripts/startup.xml")
kernel.respond("load aiml b")

# Press CTRL-C to break this loop
try:
    print(kernel.respond(sys.argv[1]))
except:
    print("Don't know that. My masters are working hard.")
sys.exit(0)


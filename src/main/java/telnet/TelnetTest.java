/**
 * Copyright 2021 XEBIALABS
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

/**
 * yyz for Toronto
 * nyc for New York
 * dca for Washington DC
 * msp for Minneapolis, St. Paul
 * ord for Chicago
 * lax for Los Angeles
 * sfo for San Francisco
 * mco for Orlando
 * mia for Miami
 * den for Denver
 * atl for Atlanta
 * bos for Boston
 */



/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package telnet;

import java.io.IOException;
import org.apache.commons.net.telnet.TelnetClient;

import telnet.*;


/***
 * This is an example of a trivial use of the TelnetClient class.
 * It connects to the weather server at the University of Michigan,
 * um-weather.sprl.umich.edu port 3000, and allows the user to interact
 * with the server via standard input.  You could use this example to
 * connect to any telnet server, but it is obviously not general purpose
 * because it reads from standard input a line at a time, making it
 * inconvenient for use with a remote interactive shell.  The TelnetClient
 * class used by itself is mostly intended for automating access to telnet
 * resources rather than interactive use.
 ***/

// This class requires the IOUtil support class!
public final class TelnetTest
{

    public static final void main(String[] args)
    {
        TelnetClient telnet;

        telnet = new TelnetClient();

        try
        {
            //telnet.connect("scn.org", 23);
            //telnet.connect("192.104.1.4", 23);
            //telnet.connect("rainmaker.wunderground.com", 3000);
            //telnet.connect("towel.blinkenlights.nl", 23);
            telnet.connect("telehack.com", 23);
        }
        catch (IOException e)
        {
            System.out.println("Caught io exception while connected");
            e.printStackTrace();
            System.exit(1);
        }

        IOUtil.readWrite(telnet.getInputStream(), telnet.getOutputStream(),
                         System.in, System.out);

        try
        {
            System.out.println("About to disconnect");
            telnet.disconnect();
        }
        catch (IOException e)
        {
            System.out.println("Caught io exception while trying to disconnect");
            e.printStackTrace();
            System.exit(1);
        }

        System.exit(0);
    }

}
//
//  SharedData.m
//  Genoma
//
//  Created by Giovanni Amati on 08/10/09.
//  Copyright 2009 __MyCompanyName__. All rights reserved.
//

#import "SharedData.h"
#import "CCDirector.h"

#define HOST "127.0.0.1"
#define PORT 66666

@implementation SharedData

-(void) dealloc
{	
	[inputStream release];
	[outputStream release];
	[DELIMETER release];
	
	NSLog(@"------------------- RELEASE SINGETON DATA ----------------------");
	
	[super dealloc];
}

-(void) connectToServer
{
	CFHostRef host;
	CFReadStreamRef readStream;
	CFWriteStreamRef writeStream;
	
	readStream = NULL;
	writeStream = NULL;
	
	host = CFHostCreateWithName(NULL, (CFStringRef)[NSString stringWithFormat:@"%s", HOST]);
	CFStreamCreatePairWithSocketToCFHost(NULL, host, PORT, &readStream, &writeStream);
	CFRelease(host);
	
	inputStream = [(NSInputStream *)readStream autorelease];
	outputStream = [(NSOutputStream *)writeStream autorelease];
	[inputStream retain];
	[outputStream retain];
	
	[inputStream setDelegate:self];
	[outputStream setDelegate:self];
	[inputStream scheduleInRunLoop:[NSRunLoop currentRunLoop] forMode:NSDefaultRunLoopMode];
	[outputStream scheduleInRunLoop:[NSRunLoop currentRunLoop] forMode:NSDefaultRunLoopMode];
	[inputStream open];
	[outputStream open];
	
	DELIMETER = [[NSString alloc] initWithString:@"\r\n"];
	[self sendToServer:[@"U|" stringByAppendingString:[[UIDevice currentDevice] uniqueIdentifier]]];
}

-(void) sendToServer:(NSString *)cmd
{
	cmd = [cmd stringByAppendingString:DELIMETER];
    [outputStream write:(const uint8_t *)[cmd UTF8String] maxLength:[cmd length]];    
}

-(void) stream:(NSStream *)stream handleEvent:(NSStreamEvent)streamEvent
{
	NSString *io;
	if (stream == inputStream) io = @"[SERVER]";
	else io = @"[CLIENT]";
	
	NSString *event;
	switch (streamEvent)
	{
		case NSStreamEventNone:
			event = @"<< EventNone >>";
			break;
		case NSStreamEventOpenCompleted:
			event = @"<< Connessione... >>";
			break;
		case NSStreamEventHasBytesAvailable:
			event = @"<< Comunicazione dati... >>";
			if (stream == inputStream)
			{
				uint8_t buffer[1024];
				unsigned int len = 0;
				while ([inputStream hasBytesAvailable])
				{
					len = [inputStream read:buffer maxLength:sizeof(buffer)];
					if (len > 0)
					{
						NSString *output = [[NSString alloc] initWithBytes:buffer length:len encoding:NSASCIIStringEncoding];
						if (nil != output)
						{
							NSArray *array_output = [output componentsSeparatedByString:DELIMETER];
							[output release];
							for (NSString *msg in array_output)
								if (![msg isEqual:@""]) [self __dispatch:msg];
						}
					}
				}
			}
			break;
		case NSStreamEventHasSpaceAvailable:
			event = @"<< Comunicazione disponibile... >>";
			break;
		case NSStreamEventErrorOccurred:
			event = @"<< Errore di connesione... >>";
			break;
		case NSStreamEventEndEncountered:
			event = @"<< Connessione persa... >>";
            [stream close];
            [stream removeFromRunLoop:[NSRunLoop currentRunLoop] forMode:NSDefaultRunLoopMode];
            //[stream release]; // libero all'uscita
			break;
		default:
			event = @"<< Sconosciuto >>";
	}
	
	NSLog(@"%@ : %@", io, event);
}

-(void) __dispatch:(NSString *)msg
{
	NSArray *arr = [msg componentsSeparatedByString:@"|"];
	
	// MENU
	if ([[arr objectAtIndex:0] isEqualToString:@"M"])
	{
		id interface = [[[CCDirector sharedDirector] runningScene] getChildByTag:1];
		NSArray *menuitems = [[arr objectAtIndex:1] componentsSeparatedByString:@";"];
		[interface initMenu:menuitems];
		NSLog(@"Menu: %@", [arr objectAtIndex:1]);
	}
	// TURN
	else if ([[arr objectAtIndex:0] isEqualToString:@"T"])
	{
		id interface = [[[CCDirector sharedDirector] runningScene] getChildByTag:1];
		[interface setTurn:[arr objectAtIndex:1]];
		NSLog(@"Turn: %@", [arr objectAtIndex:1]);
	}
	// CHARACTER
	else if ([[arr objectAtIndex:0] isEqualToString:@"P1"])
	{
		id game = [[[CCDirector sharedDirector] runningScene] getChildByTag:0];
		int pos = 1;
		NSArray *chrs = [[arr objectAtIndex:1] componentsSeparatedByString:@";"];
		for (NSString *c in chrs)
		{
			NSArray *attr = [c componentsSeparatedByString:@","];
			[game addMyCharacter:attr position:pos];
			pos = pos + 1;
		}
	}
	else if ([[arr objectAtIndex:0] isEqualToString:@"P2"])
	{
		id game = [[[CCDirector sharedDirector] runningScene] getChildByTag:0];
		int pos = 1;
		NSArray *chrs = [[arr objectAtIndex:1] componentsSeparatedByString:@";"];
		for (NSString *c in chrs)
		{
			NSArray *attr = [c componentsSeparatedByString:@","];
			[game addEnemyCharacter:attr position:pos];
			pos = pos + 1;
		}
	}
	// ECHO
	else if ([[arr objectAtIndex:0] isEqualToString:@"E"])
	{
		UIAlertView *alert = [[UIAlertView alloc] initWithTitle:@"Message" message:[arr objectAtIndex:1] delegate:self cancelButtonTitle:@"Cancel" otherButtonTitles:@"Ok", nil];
		[alert show];
		[alert release];
	}
	// NOT IMPLEMENTED
	else
		NSLog(@"Not implemented: %@", arr);
}

-(void) alertView:(UIAlertView *)actionSheet clickedButtonAtIndex:(NSInteger)buttonIndex
{
	// the user clicked one of the OK/Cancel buttons
	if (buttonIndex == 1)
	{
		NSLog(@"Ok");
	}
	else
	{
		NSLog(@"Cancel");
	}
}

-(void) menu:(int)i
{
	[self sendToServer:[@"M|" stringByAppendingFormat:@"%D", i]];
}

/////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////// Singleton ///////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////

static SharedData *sharedMyData = nil;

+(SharedData *) Initialize
{
    @synchronized(self)
	{
        if (sharedMyData == nil)
		{
            [[self alloc] init];
        }
    }
	
    return sharedMyData;
}

+(id) allocWithZone:(NSZone *)zone
{
    @synchronized(self)
	{
        if (sharedMyData == nil)
		{
            sharedMyData = [super allocWithZone:zone];
            return sharedMyData;
        }
    }
	
    return nil;
}

-(id) copyWithZone:(NSZone *)zone
{	
    return self;
}

-(id) retain
{
    return self;
}

-(unsigned) retainCount
{
    return UINT_MAX;
}

-(void) release
{
	[super release];
}

-(id) autorelease
{
	return self;
}

@end
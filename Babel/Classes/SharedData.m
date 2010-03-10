// This file is part of babel4iphone.

// Copyright (C) 2009 Giovanni Amati <amatig@gmail.com>

// babel4iphone is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// babel4iphone is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with babel4iphone.  If not, see <http://www.gnu.org/licenses/>.


#import "SharedData.h"

@implementation SharedData

-(void) dealloc
{	
	[inputStream release];
	[outputStream release];
	
	sqlite3_close(database);
	
	NSLog(@"------------------- RELEASE SINGETON DATA ----------------------");
	
	[super dealloc];
}

-(void) __copyDatabaseToDocuments:(NSString *)databasePath named:(NSString *)databaseName
{
	// Create a FileManager object
	NSFileManager *fileManager = [NSFileManager defaultManager];
	// Get the path to the database in the application package
	NSString *databasePathFromApp = [[[NSBundle mainBundle] resourcePath] stringByAppendingPathComponent:databaseName];
	// Check if the database already exists then remove it
	BOOL success = [fileManager fileExistsAtPath:databasePath];
	if (success)
	{
		if ([fileManager contentsEqualAtPath:databasePathFromApp andPath:databasePath] == YES)
			NSLog(@"SQLITE Same database");
		else
		{
			[fileManager removeItemAtPath:databasePath error:nil];
			success = FALSE;
			NSLog(@"SQLITE Remove database");
		}
	}
	if (!success)
	{
		// Copy the database from the package to the users filesystem
		[fileManager copyItemAtPath:databasePathFromApp toPath:databasePath error:nil];
		NSLog(@"SQLITE Copy new database");
	}
	
	[fileManager release];
}

-(void) connectToDatabase
{
	NSString *databaseName = [NSString stringWithFormat:@"%s", DATABASE];
	NSArray *documentPaths = NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES);
	NSString *documentsDir = [documentPaths objectAtIndex:0];
	NSString *databasePath = [documentsDir stringByAppendingPathComponent:databaseName];
	
	[self __copyDatabaseToDocuments:databasePath named:databaseName];
	
	if (sqlite3_open([databasePath UTF8String], &database) != SQLITE_OK)
		NSAssert1(0, @"SQLITE Error db. '%s'", sqlite3_errmsg(database));
}

-(NSMutableArray *) execQuery:(NSString *)sqlStatement
{
	NSMutableArray *result = [NSMutableArray array];
	
	// Setup the SQL Statement and compile it for faster access
	sqlite3_stmt *compiledStatement;
	if (sqlite3_prepare_v2(database, [sqlStatement UTF8String], -1, &compiledStatement, NULL) == SQLITE_OK)
	{
		// Loop through the results and add them to the feeds array
		while (sqlite3_step(compiledStatement) == SQLITE_ROW)
		{
			int cols = sqlite3_column_count(compiledStatement);
			for (int i = 0; i < cols; i++)
			{
				// Read the data from the result row
				NSString *tmp = [NSString stringWithUTF8String:(char *)sqlite3_column_text(compiledStatement, i)];
				[result addObject:tmp];
			}
		}
	}
	else
		NSAssert1(0, @"SQLITE Error db. '%s'", sqlite3_errmsg(database));
	// Release the compiled statement from memory
	sqlite3_finalize(compiledStatement);
	
	return result;
}

-(NSMutableArray *) getCharInfo:(NSString *)race job:(NSString *)job level:(int)level supjob:(NSString *)supjob suplevel:(int)suplevel
{
	NSMutableArray *row = [NSMutableArray array];
	
	int sl = level / 2;
	if (sl < 1) sl = 1;
	if (sl > suplevel) sl = suplevel;
	
	NSMutableArray *infoRACE = [self execQuery:[NSString stringWithFormat:@"SELECT * FROM type where id='%@'", race]];
	NSMutableArray *infoJOB = [self execQuery:[NSString stringWithFormat:@"SELECT * FROM type where id='%@'", job]];
	NSMutableArray *infoSUPJOB = NULL;
	if (![supjob isEqualToString:@"None"])
		infoSUPJOB = [self execQuery:[NSString stringWithFormat:@"SELECT * FROM type where id='%@'", supjob]];
	
	NSMutableArray *infoRHP = [self execQuery:[NSString stringWithFormat:@"SELECT * FROM scale where id='%@'", [infoRACE objectAtIndex:1]]];
	int rhp = [CoreFunctions scaleHP:[[infoRHP objectAtIndex:1] floatValue] 
							  baseHP:[[infoRHP objectAtIndex:2] floatValue] 
						  scaleHPxXx:[[infoRHP objectAtIndex:3] floatValue] 
							   level:level];
	
	NSMutableArray *infoJHP = [self execQuery:[NSString stringWithFormat:@"SELECT * FROM scale where id='%@'", [infoJOB objectAtIndex:1]]];
	int jhp = [CoreFunctions scaleHP:[[infoJHP objectAtIndex:1] floatValue] 
							  baseHP:[[infoJHP objectAtIndex:2] floatValue] 
						  scaleHPxXx:[[infoJHP objectAtIndex:3] floatValue] 
							   level:level
								 job:[infoJOB objectAtIndex:0]];
	
	int sjhp = 0;
	if (infoSUPJOB)
	{
		NSMutableArray *infoSJHP = [self execQuery:[NSString stringWithFormat:@"SELECT * FROM scale where id='%@'", [infoSUPJOB objectAtIndex:1]]];
		sjhp = [CoreFunctions scaleHP:[[infoSJHP objectAtIndex:1] floatValue] 
							   baseHP:[[infoSJHP objectAtIndex:2] floatValue] 
							 suplevel:sl
							   supjob:[infoSUPJOB objectAtIndex:0]];
	}
	
	// HP
	[row addObject:[NSNumber numberWithInteger:rhp + jhp + sjhp]];
	
	BOOL mp_not_available_job = [[infoJOB objectAtIndex:2] isEqualToString:@"X"];
	BOOL mp_not_available_supjob = YES;
	if (infoSUPJOB)
		mp_not_available_supjob = [[infoSUPJOB objectAtIndex:2] isEqualToString:@"X"];
	
	int lm = level;
	if (mp_not_available_job)
		lm = sl;
	
	int rmp = 0;
	if (!mp_not_available_job || !mp_not_available_supjob)
	{
		NSMutableArray *infoRMP = [self execQuery:[NSString stringWithFormat:@"SELECT * FROM scale where id='%@'", [infoRACE objectAtIndex:2]]];
		rmp = [CoreFunctions scaleMP:[[infoRMP objectAtIndex:4] floatValue] 
							  baseMP:[[infoRMP objectAtIndex:5] floatValue]  
							 levelMP:lm];
	}
	
	int jmp = 0;
	if (!mp_not_available_job)
	{
		NSMutableArray *infoJMP = [self execQuery:[NSString stringWithFormat:@"SELECT * FROM scale where id='%@'", [infoJOB objectAtIndex:2]]];
		jmp = [CoreFunctions scaleMP:[[infoJMP objectAtIndex:4] floatValue] 
							  baseMP:[[infoJMP objectAtIndex:5] floatValue]  
							 levelMP:lm
							   level:level
								 job:[infoJOB objectAtIndex:0]];
	}
	
	int sjmp = 0;
	if (!mp_not_available_supjob)
	{
		NSMutableArray *infoSJMP = [self execQuery:[NSString stringWithFormat:@"SELECT * FROM scale where id='%@'", [infoSUPJOB objectAtIndex:2]]];
		sjmp = [CoreFunctions scaleMP:[[infoSJMP objectAtIndex:4] floatValue] 
							   baseMP:[[infoSJMP objectAtIndex:5] floatValue]  
							 suplevel:sl
							   supjob:[infoSUPJOB objectAtIndex:0]];
	}
	
	int mp = 0;
	if (!mp_not_available_job)
		mp = rmp + jmp + sjmp;
	else if (!mp_not_available_supjob)
		mp = (int)(rmp / 2) + sjmp;
	
	// MP
	[row addObject:[NSNumber numberWithInteger:mp]];
	
	for (int a = 3; a < 9; a++)
	{
		NSMutableArray *statsRACE = [self execQuery:[NSString stringWithFormat:@"SELECT * FROM scale where id='%@'", [infoRACE objectAtIndex:a]]];
		int star = [CoreFunctions scaleSTATS:[[statsRACE objectAtIndex:6] floatValue] 
								   baseSTATS:[[statsRACE objectAtIndex:7] floatValue]  
									   level:level];
		
		NSMutableArray *statsJOB = [self execQuery:[NSString stringWithFormat:@"SELECT * FROM scale where id='%@'", [infoJOB objectAtIndex:a]]];
		int staj = [CoreFunctions scaleSTATS:[[statsJOB objectAtIndex:6] floatValue] 
								   baseSTATS:[[statsJOB objectAtIndex:7] floatValue]  
									   level:level];
		
		int stasj = 0;
		if (infoSUPJOB)
		{
			NSMutableArray *statsSUPJOB = [self execQuery:[NSString stringWithFormat:@"SELECT * FROM scale where id='%@'", [infoSUPJOB objectAtIndex:a]]];
			stasj = [CoreFunctions scaleSTATS:[[statsSUPJOB objectAtIndex:6] floatValue] 
									baseSTATS:[[statsSUPJOB objectAtIndex:7] floatValue]  
										level:sl];
		}
		int statsA = star + staj + (int)(stasj / 2);
		
		// STATS
		[row addObject:[NSNumber numberWithInteger:statsA]];
	}
	
	return row;
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
	
	[self sendToServer:[NSString stringWithFormat:@"U|%@", [[UIDevice currentDevice] uniqueIdentifier]]];
}

-(void) sendToServer:(NSString *)cmd
{
	cmd = [cmd stringByAppendingString:[NSString stringWithFormat:@"%s", DELIMETER]];
    [outputStream write:(const uint8_t *)[cmd UTF8String] maxLength:[cmd length]];
}

-(void) stream:(NSStream *)stream handleEvent:(NSStreamEvent)streamEvent
{
	NSString *io;
	if (stream == inputStream)
		io = @"[SERVER]";
	else
		io = @"[CLIENT]";
	
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
							NSArray *array_output = [output componentsSeparatedByString:[NSString stringWithFormat:@"%s", DELIMETER]];
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
	id game = [[[CCDirector sharedDirector] runningScene] getChildByTag:0];
	id interface = [[[CCDirector sharedDirector] runningScene] getChildByTag:1];
	
	NSArray *arr = [msg componentsSeparatedByString:@"|"];
	
	// MENU
	if ([[arr objectAtIndex:0] isEqualToString:@"M"])
	{
		NSArray *menuitems = [[arr objectAtIndex:1] componentsSeparatedByString:@";"];
		[interface initMenu:menuitems];
		NSLog(@"Menu: %@", [arr objectAtIndex:1]);
	}
	// TURN
	else if ([[arr objectAtIndex:0] isEqualToString:@"T"])
	{
		[interface setTurn:[arr objectAtIndex:1]];
		NSLog(@"Turn: %@", [arr objectAtIndex:1]);
	}
	// ANIM FIGHT
	else if ([[arr objectAtIndex:0] isEqualToString:@"A"])
	{
		[game playFight];
		NSLog(@"play fight: %@", [arr objectAtIndex:1]);
	}
	// CHARACTER
	else if ([[arr objectAtIndex:0] isEqualToString:@"P1"])
	{
		int pos = 1;
		NSArray *chrs = [[arr objectAtIndex:1] componentsSeparatedByString:@";"];
		for (NSString *c in chrs)
		{
			NSArray *info = [c componentsSeparatedByString:@","];
			[game addMyCharacter:info position:pos];
			pos = pos + 1;
		}
	}
	else if ([[arr objectAtIndex:0] isEqualToString:@"P2"])
	{
		int pos = 1;
		NSArray *chrs = [[arr objectAtIndex:1] componentsSeparatedByString:@";"];
		for (NSString *c in chrs)
		{
			NSArray *info = [c componentsSeparatedByString:@","];
			[game addEnemyCharacter:info position:pos];
			pos = pos + 1;
		}
	}
	// ECHO
	else if ([[arr objectAtIndex:0] isEqualToString:@"E"])
	{
		UIAlertView *alert = [[UIAlertView alloc] initWithTitle:@"Alert" message:[arr objectAtIndex:1] delegate:self cancelButtonTitle:@"Cancel" otherButtonTitles:@"Ok", nil];
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
		NSLog(@"Ok on %@", [actionSheet title]);
	}
	else
	{
		NSLog(@"Cancel on %@", [actionSheet title]);
	}
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
